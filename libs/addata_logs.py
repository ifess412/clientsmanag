
action_tag = {1: "add", 2: "edit", 3: "delete"}
logmess = {"add":"Додано запис в БД.", "edit":"Змінено запис в БД.", "delete":"Видалено запис з БД."}

# id, app_label, obj_model, obj_id, mess, action_tag, user_id, date_time
# table_nomenclature = {
#     "id": "ID",
#     "name": "Назва",
#     "fullname": "Повна назва",
#     "code": "Код",
#     "type": "Тип",
#     "tag": "Тег",
#     "pk": "Дії",
# }

mdlnames = {
    # "tags": "Теги",
    # "tag": "Тег",
    # "accesses": "Доступи",
    # "access": "Доступ",
    # "contacts": "Контакти",
    # "contact": "Контакт",
    # "clients": "Кліенти",
    # "client": "Кліент",
    "islogs": "Logs",
    "islog": "Log",
}

table_logs = [
    "ID",
    "Повідомлення",
    "Тип запису",
    "Дата",
    "Користувач",
    "Дії",
]

table_admlogs = [
    "ID",
    "Модуль",
    "Модель",
    "ІД запису",
    "Повідомлення",
    "Тип запису",
    "Дата",
    "Користувач",
    "Дії",
]