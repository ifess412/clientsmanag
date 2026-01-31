# В цьому файлі додаткова бібліотека необхідних данних
mdlnames = {
    "tags": "Теги",
    "tag": "Тег",
    "accesses": "Доступи",
    "access": "Доступ",
    "contacts": "Контакти",
    "contact": "Контакт",
    "clients": "Кліенти",
    "client": "Кліент",
    "islogs": "Logs",
    "islog": "Log",
    "cities": "Міста",
    "city": "Місто",
}

client_type = {0: "my_org", 1: "клієнт", 2: "партнер"}

app_names = {
    "AD": "AnyDesk",
    "AA": "Ammy Admin",
    "TV": "Team Viewer",
    "RDP": "Remote Desktop Protocol",
    "Other": "Other app",
}

action_tag = {1: "add", 2: "edit", 3: "delete"}

logmess = {"add":"Додано запис в БД.", "edit":"Змінено запис в БД.", "delete":"Видалено запис з БД."}

# id, name, fullname, code, address, comment, type, tags, slug 
# + contacts, accesses
table_clients = {
    "id": "ID",
    "code":"ЄДРПОУ",
    "name":"Назва",
    "fullname":"Повна назва",
    "type":"Тип",
    "address":"Адреса",
    "comment":"Коммент",
    "tags":"Теги",
    "contacts":"Контакти",
    "accesses":"Доступи",
    "pk":"Дії",
}

# card_clients = [
#     "ID",
#     "Назва",
#     "ЄДРПОУ",
#     "Повна назва",
#     "Тип",
#     "Адреса",
#     "Коммент",
#     "Теги",
#     "Контакти",
#     "Доступи",
#     "URL",
# ]


# id, name, phone1, phone2, phone3, email, comment, client, position, order, slug
table_contacts = {
    "id": "ID",
    "name":"ПІБ",
    "phone1":"Телефони",
    "email":"Еmail",
    "client":"Клієнт",
    "position":"Посада",
    "order": "Порядок",
    "comment": "Коммент",
    "pk": "Дії",
}

# id, name, app, idinapp, passinapp, comment, client, order, slug
table_accesses = {
    "id": "ID",
    "name": "Назва",
    "client": "Клієнт",
    "app": "Застосунок",
    "idinapp": "ID доступу",
    "passinapp": "Пароль",
    "order": "Порядок",
    "comment": "Коммент",
    "pk": "Дії",
}

# id, title, color, slug
table_tags = {
    "id": "ID",
    "title": "Назва",
    "color": "Колір",
    "example": "Приклад",
    "pk": "Дії",
}

# id, name,
table_cities = {
    "id": "ID",
    "name": "Назва",
    "pk": "Дії",
}

# id, name,
table_citydistr = {
    "id": "ID",
    "name": "Назва",
    "pk": "Дії",
}

# id, name, fullname, distr, archive
table_street = {
    "id": "ID",
    "name": "Назва",
    "fullname": "Повна назва",
    "distr": "Район міста",
    "archive": "Архівний",
    "pk": "Дії",
}

    # client, addresstype, index, country, region, settltype, cityname, ​distr, 
    # streettype, streetname, oldstreetname, housenum, apartmenttype, apartment, entrance, floor, comment
table_fulladdress = {
    "id": "ID",
    "client": "Кліент",
    "addresstype": "Тип адреси",
    "index": "Індекс",
    "country": "Країна",
    "region": "Область",
    "settltype": "Тип населенного пункту",
    "cityname": "Місто",
    "distr": "Район міста",
    "streettype": "Тип вулиці",
    "streetname": "Назва вулиці",
    "oldstreetname": "Стара назва вулиці",
    "housenum": "Будинок",
    "apartmenttype": "Тип квартира/офіс",
    "apartment": "Номер кв./оф.",
    "entrance": "Під'їзд",
    "floor": "Поверх",
    "comment": "Коментар",
    "pk": "Дії",
}