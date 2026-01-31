# for logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .middleware import get_current_request

from .models import Client, Contact, Access, Tag, City, Distr, Street, Fulladdress

from logs.models import Islog
from libs.logs_adddata import logmess
# from logs.signals import islog_add_record




# logging 1
# @receiver(post_save, sender=Client)
# def log_new_record(sender, instance, created, **kwargs):
#     print(sender)
#     obj_model = 'clients_client'
#     obj_id = instance.pk
#     # print(instance)
#     request = get_current_request()
#     if request and request.user.is_authenticated:
#         usrid = request.user.id
#     else:
#         usrid= 0
#     # print("userid ",usrid)
#     if created:
#         mess = logmess['add']
#         action_tag = 1
#         #logger.info(f"Создана новая запись в {sender.__name__}: {instance}")
#     else:
#         #logger.info(f"Обновлена запись в {sender.__name__}: {instance}")
#         mess = logmess['edit']
#         action_tag = 2
#     new=Islog.objects.create(obj_model=obj_model, obj_id=obj_id, action_tag=action_tag, mess=mess, user_id=usrid)
#     print("Add new row in islog table ",new.pk)


APPL = 'clients'

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


# def islog_new_record_client(sender, instance, created, deleted = False, **kwargs):
#     # sendapp = 'clients'
#     sendmdl = 'client'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_new_record_contact(sender, instance, created, deleted = False, **kwargs):
#     # sendapp = 'clients'
#     sendmdl = 'contact'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_new_record_access(sender, instance, created, deleted = False, **kwargs):
#     # sendapp = 'clients'
#     sendmdl = 'access'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_new_record_tag(sender, instance, created, deleted = False, **kwargs):
#     # sendapp = 'clients'
#     sendmdl = 'tag'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)


# def islog_del_record_client(sender, instance, created = False, deleted = True, **kwargs):
#     # sendapp = APPL
#     sendmdl = 'client'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_del_record_contact(sender, instance, created = False, deleted = True, **kwargs):
#     # sendapp = APPL
#     sendmdl = 'contact'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_del_record_access(sender, instance, created = False, deleted = True, **kwargs):
#     # sendapp = APPL
#     sendmdl = 'access'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

# def islog_del_record_tag(sender, instance, created = False, deleted = True, **kwargs):
#     # sendapp = APPL
#     sendmdl = 'tag'
#     islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)


def islog_new_record(sender, instance, created, deleted = False, **kwargs):
    sendmdl = instance._meta.model_name
    islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)

def islog_new_record_del(sender, instance, created = False, deleted = True, **kwargs):
    sendmdl = instance._meta.model_name
    islog_add_record(sender, instance, created, deleted, sendmdl, **kwargs)


post_save.connect(islog_new_record, sender=Client)
post_delete.connect(islog_new_record_del, sender=Client)

post_save.connect(islog_new_record, sender=Contact)
post_delete.connect(islog_new_record_del, sender=Contact)

post_save.connect(islog_new_record, sender=Access)
post_delete.connect(islog_new_record_del, sender=Access)

post_save.connect(islog_new_record, sender=Tag)
post_delete.connect(islog_new_record_del, sender=Tag)

post_save.connect(islog_new_record, sender=City)
post_delete.connect(islog_new_record_del, sender=City)

post_save.connect(islog_new_record, sender=Distr)
post_delete.connect(islog_new_record_del, sender=Distr)

post_save.connect(islog_new_record, sender=Street)
post_delete.connect(islog_new_record_del, sender=Street)

post_save.connect(islog_new_record, sender=Fulladdress)
post_delete.connect(islog_new_record_del, sender=Fulladdress)