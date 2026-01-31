# for logging
from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

from clients.middleware import get_current_request

from .models import Nomenclature, Price, Balance, Discount

from logs.models import Islog
from libs.logs_adddata import logmess
# from logs.signals import islog_add_record

APPL = 'finances'

# logging 
def islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs):
    app_label = APPL
    # app_label = sendapp
    obj_model = sendmdl
    obj_id = instance.pk
    request = get_current_request()
    if request and request.user.is_authenticated:
        usrid = request.user.id
    else:
        usrid = 0
    if created:
        mess = logmess['add']
        action_tag = 1
    else:
        if deleted:
            mess = logmess['delete']
            action_tag = 3
        else:
            mess = logmess['edit']
            action_tag = 2
    new=Islog.objects.create(app_label=app_label, obj_model=obj_model, obj_id=obj_id, action_tag=action_tag, mess=mess, user_id=usrid)



# def islog_new_record_nomenclature(sender, instance, created, deleted = False, **kwargs):
#     # sendapp = APPL
#     sendmdl = 'nomenclature'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_new_record_nomenclature_del(sender, instance, created = False, deleted = True, **kwargs):
#     # sendapp = APPL
#     sendmdl = 'nomenclature'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)


# post_save.connect(islog_new_record_nomenclature, sender=Nomenclature)
# post_delete.connect(islog_new_record_nomenclature_del, sender=Nomenclature)

def islog_new_record(sender, instance, created, deleted = False, **kwargs):
    sendmdl = instance._meta.model_name
    islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

def islog_new_record_del(sender, instance, created = False, deleted = True, **kwargs):
    sendmdl = instance._meta.model_name
    islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)


post_save.connect(islog_new_record, sender=Nomenclature)
post_delete.connect(islog_new_record_del, sender=Nomenclature)

post_save.connect(islog_new_record, sender=Price)
post_delete.connect(islog_new_record_del, sender=Price)

post_save.connect(islog_new_record, sender=Balance)
post_delete.connect(islog_new_record_del, sender=Balance)

post_save.connect(islog_new_record, sender=Discount)
post_delete.connect(islog_new_record_del, sender=Discount)
