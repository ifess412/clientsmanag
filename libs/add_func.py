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
    # sf = checkSlugField(model)
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


