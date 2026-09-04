from django.http import HttpResponse
from openpyxl import Workbook

from django.db.models import Q


# def checkSlugField(model):
#     # Получение имен полей модели
#     column_names = [field.name for field in model._meta.get_fields() if hasattr(field, 'name')]
#     slugfield = False
#     checkname = 'slug'
#     if checkname in column_names:
#         slugfield = True
#     else:
#         slugfield = False
#     return slugfield

def checkFieldExist(model, field):
    # Получение имен полей модели
    column_names = [field.name for field in model._meta.get_fields() if hasattr(field, 'name')]
    res = False
    checkname = str(field)
    if checkname in column_names:
        res = True
    else:
        res = False
    return res

def getOneObj(model, instance, params=False):
    if isinstance(instance, str):
        # Do something with the string
        # print("Value is a string:", instance)
        sf = checkFieldExist(model, 'slug')
        if sf :
            obj_obj = model.objects.get(slug=instance)
        else : 
            obj_obj = model.objects.get(pk=int(instance))
            # pass
    # Check if 'value' is an instance of a specific Django model, e.g., MyModel
    # elif isinstance(instance, model):
    #     # Do something with the model instance
    #     print("Value is a MyModel instance:", instance.field_name)
    #     sf = checkFieldExist(model, 'slug')
    #     if sf :
    #         obj_obj = model.objects.get(slug=instance.kwargs["slug"])
    #     else : 
    #         obj_obj = model.objects.get(pk=instance.kwargs["pk"])
    else:
        # Handle other types
        # print("Value is neither a string nor a MyModel instance")
        # obj_obj = 0
        sf = checkFieldExist(model, 'slug')
        if sf :
            obj_obj = model.objects.get(slug=instance.kwargs["slug"])
        else : 
            obj_obj = model.objects.get(pk=instance.kwargs["pk"])
    return obj_obj

def export_to_excel(instance, YourModel, orderby='pk', filterrows=''):
    queryset = YourModel.objects.all() # Ваши данные
    if orderby:
        queryset = queryset.order_by(orderby)
    if filterrows:
        queryset = queryset.filter(
            Q(name__icontains=filterrows)
            | Q(client__slug=filterrows)
        )


    wb = Workbook()
    ws = wb.active
    ws.title = "Экспорт данных"

    # Заголовки
    # headers = [f.name for f in YourModel._meta.fields]
    headers = [f.verbose_name for f in YourModel._meta.fields]
    ws.append(headers)

    # Строки
    for item in queryset:
        # row = [getattr(item, field.name) for field in YourModel._meta.fields]
        results = []
        for field in YourModel._meta.fields:
            value = getattr(item, field.name)
            if field.is_relation and value is not None:
                # Це поле ForeignKey (або інший тип відношення), отримуємо потрібний атрибут
                # Тут ми припускаємо, що ви хочете отримати атрибут 'name'
                results.append(getattr(value, 'name', str(value))) 
            else:
                # Звичайне поле
                results.append(value)
        row = results
        ws.append(row)

    # Создание ответа для скачивания
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
    wb.save(response)
    return response

def get_columnames(formodel):
    columnames = {
    }
    for f in formodel._meta.fields:
        columnames[f.name] = f.verbose_name
    # columnames = [f.verbose_name for f in model._meta.fields]
    columnames['pk'] = 'Дії'
    return columnames

def balance_get_or_update(model, client, sum):
    balobj, bcreated = model.objects.get_or_create(client=client)
    if sum!=0 :
        balobj.balance += sum
        balobj.save()  # Зберігаємо зміни
    return balobj.balance


