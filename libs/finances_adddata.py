# В цьому файлі додаткова бібліотека необхідних данних

nomenclature_type = {1: "ліцензія", 2: "послуга", 3: "товар"}

# id, name, fullname, code, address, comment, type, tags, slug
table_nomenclature = {
    "id": "ID",
    "code": "Код",
    "name": "Назва",
    "fullname": "Повна назва",
    "type": "Тип",
    "tag": "Тег",
    "pk": "Дії",
}

# table_price = {
#     "id": "ID",
#     "nomenclature__code": "Код",
#     "nomenclature": "Номенклатура",
#     "price": "Ціна",
#     "date_time": "Дата",
#     "pk": "Дії",
# }

table_price = {
    "id": "ID",
    "code": "Код",
    "name": "Номенклатура",
    # "name": "Номенклатура",
    "prices__price": "Ціна",
    "prices__datetime": "Дата",
    "pk": "Дії",
}

table_discount = {
    "id": "ID",
    "code": "ЄДРПОУ",
    "name": "Назва",
    "fullname": "Повна назва",
    "discount__discount": "Знижка",
    "discount__datetime": "Дата",
    "pk": "Дії",
}

table_balance = {
    "id": "ID",
    "client__code": "ЄДРПОУ",
    "client__name": "Назва",
    "client__fullname": "ПОвна назва",
    "balance": "Баланс",
    "discount": "Знижка",
    "pk": "Дії",
}

mdlnames = {
    "nomenclature": "Номенклатура",
    "nomenclatures": "Номенклатура",
    "price": "Прайс",
    "prices": "Прайси",
    "balance": "Баланс",
    "discount": "Знижки",
}
