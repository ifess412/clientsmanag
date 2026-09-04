# for logging
from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

from clients.middleware import get_current_request

# from .models import Nomenclature, Price, Balance, Discount, Cashbook, Transaction
from .models import *

from logs.models import Islog
# from libs.logs_adddata import logmess
from libs.addata_logs import logmess
from libs.add_func import balance_get_or_update
# from logs.signals import islog_add_record

APPL = 'finances'

# transaction
def transaction_create(docdate, client, sum, docapp, docmodel, docid):
    new=Transaction.objects.create(docdate=docdate, client=client, sum=sum, docapp=docapp, docmodel=docmodel, docid=docid)
    return new 

def transaction_delete(client, docapp, docmodel, docid):
    # obj = Transaction.objects.get(client=client, docapp=docapp, docmodel=docmodel, docid=docid)
    obj = Transaction.objects.filter(client=client, docapp=docapp, docmodel=docmodel, docid=docid).first()
    if obj is not None:
        obj.delete()
        res = obj.sum
    else: res = 0
    return res

# def balance_update(client_id, sum):
#     balobj, bcreated = Balance.objects.get_or_create(client=client_id)
#     balobj.balance += sum
#     balobj.save()  # Зберігаємо зміни
#     return balobj.balance

def transaction_add_record(sender, instance, created, deleted, **kwargs):
    app_label = APPL
    balmodel = Balance
    # app_label = sendapp
    # obj_model = sendmdl
    obj_model = instance._meta.model_name
    obj_id = instance.pk
    if created:
        # mess = logmess['add']
        if obj_model == 'cashbook':
            docdate = instance.datedoc
            isum = instance.sum
            # -100
            clientid = instance.payer
            sum = isum * (-1)
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # +100
            clientid = instance.payee
            sum = isum
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
        if obj_model == 'license':
            docdate = instance.orderdate
            # client
            clientid = instance.client
            price = instance.price
            sum = price
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # dev
            clientid = instance.developer
            price = instance.devprice
            sum = price * (-1)
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # agent
            clientid = instance.agent
            price = instance.agprice
            sum = price * (-1)
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # taxes
            clientid = instance.taxes
            price = instance.taxprice
            sum = price * (-1)
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
        if obj_model == 'act':
            docdate = instance.datedoc
            # client
            clientid = instance.client
            price = instance.price
            sum = price
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # dev
            # clientid = instance.developer
            # price = instance.devprice
            # sum = price * (-1)
            # updbalance = balance_get_or_update(balmodel, clientid, sum)
            # new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # agent
            clientid = instance.agent
            price = instance.agprice
            sum = price * (-1)
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            # taxes
            clientid = instance.taxes
            price = instance.taxprice
            sum = price * (-1)
            updbalance = balance_get_or_update(balmodel, clientid, sum)
            new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)

    else:
        if deleted:
            # mess = logmess['delete']
            if obj_model == 'cashbook':
                isum = instance.sum
                clientid = instance.payer
                # +100
                sum = isum 
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
                # -100
                clientid = instance.payee
                sum = isum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
            if obj_model == 'license':
                # docdate = instance.orderdate
                # client
                clientid = instance.client
                price = instance.price
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
                # dev
                clientid = instance.developer
                price = instance.devprice
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
                # agent
                clientid = instance.agent
                price = instance.agprice
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
                # taxes
                clientid = instance.taxes
                price = instance.taxprice
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
            if obj_model == 'act':
                # docdate = instance.orderdate
                # client
                clientid = instance.client
                price = instance.price
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
                # dev
                # clientid = instance.developer
                # price = instance.devprice
                # sum = price
                # updbalance = balance_get_or_update(balmodel, clientid, sum)
                # transaction_delete(clientid, app_label, obj_model, obj_id)
                # agent
                clientid = instance.agent
                price = instance.agprice
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)
                # taxes
                clientid = instance.taxes
                price = instance.taxprice
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                transaction_delete(clientid, app_label, obj_model, obj_id)

        else:
            # mess = logmess['edit']
            if obj_model == 'cashbook':
                # delete old transactions
                clientid = instance.payer
                # +100
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # -100
                clientid = instance.payee
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # add new transactions
                docdate = instance.datedoc
                isum = instance.sum
                # -100
                clientid = instance.payer
                sum = isum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # +100
                clientid = instance.payee
                sum = isum
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            if obj_model == 'license':
                # delete old transactions
                clientid = instance.client
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # dev
                clientid = instance.developer
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # agent
                clientid = instance.agent
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # taxes
                clientid = instance.taxes
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)

                # add new transactions
                docdate = instance.orderdate
                # client
                clientid = instance.client
                price = instance.price
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # dev
                clientid = instance.developer
                price = instance.devprice
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # agent
                clientid = instance.agent
                price = instance.agprice
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # taxes
                clientid = instance.taxes
                price = instance.taxprice
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
            if obj_model == 'act':
                # delete old transactions
                clientid = instance.client
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # dev
                # clientid = instance.developer
                # dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                # sum = dsum * (-1)
                # updbalance = balance_get_or_update(balmodel, clientid, sum)
                # agent
                clientid = instance.agent
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                # taxes
                clientid = instance.taxes
                dsum = transaction_delete(clientid, app_label, obj_model, obj_id)
                sum = dsum * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)

                # add new transactions
                docdate = instance.datedoc
                # client
                clientid = instance.client
                price = instance.price
                sum = price
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # dev
                # clientid = instance.developer
                # price = instance.devprice
                # sum = price * (-1)
                # updbalance = balance_get_or_update(balmodel, clientid, sum)
                # new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # agent
                clientid = instance.agent
                price = instance.agprice
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)
                # taxes
                clientid = instance.taxes
                price = instance.taxprice
                sum = price * (-1)
                updbalance = balance_get_or_update(balmodel, clientid, sum)
                new = transaction_create(docdate, clientid, sum, app_label, obj_model, obj_id)


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

def transaction_new_record(sender, instance, created, deleted = False, **kwargs):
    # sendmdl = instance._meta.model_name
    transaction_add_record(sender, instance, created, deleted, **kwargs)

def transaction_new_record_del(sender, instance, created = False, deleted = True, **kwargs):
    # sendmdl = instance._meta.model_name
    transaction_add_record(sender, instance, created, deleted, **kwargs)


post_save.connect(islog_new_record, sender=Nomenclature)
post_delete.connect(islog_new_record_del, sender=Nomenclature)

post_save.connect(islog_new_record, sender=Price)
post_delete.connect(islog_new_record_del, sender=Price)

post_save.connect(islog_new_record, sender=Balance)
post_delete.connect(islog_new_record_del, sender=Balance)

post_save.connect(islog_new_record, sender=Discount)
post_delete.connect(islog_new_record_del, sender=Discount)

post_save.connect(islog_new_record, sender=Cashbook)
post_delete.connect(islog_new_record_del, sender=Cashbook)

post_save.connect(transaction_new_record, sender=Cashbook)
post_delete.connect(transaction_new_record_del, sender=Cashbook)

post_save.connect(islog_new_record, sender=License)
post_delete.connect(islog_new_record_del, sender=License)

post_save.connect(transaction_new_record, sender=License)
post_delete.connect(transaction_new_record_del, sender=License)

post_save.connect(islog_new_record, sender=Act)
post_delete.connect(islog_new_record_del, sender=Act)

post_save.connect(transaction_new_record, sender=Act)
post_delete.connect(transaction_new_record_del, sender=Act)
