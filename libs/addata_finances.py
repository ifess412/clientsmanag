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
    "code": "ЄДРПОУ",
    "name": "Назва",
    "fullname": "Повна назва",
    "balance__balance": "Баланс",
    "pk": "Дії",
}

# id, num, datedoc, payer, payee, sum, paytype, paystatus, comment
table_cashbook = {
    "id": "ID",
    "num": "Номер",
    "datedoc": "Дата",
    "payer": "Платник",
    "payee": "Отримувач",
    "sum": "Сума",
    "paytype": "Тип",
    "paystatus": "Статус",
    "comment": "Коментар",
    "pk": "Дії",
}

# 'id', 'client', 'sum', 'datetime', 'balance', 'docapp', 'docmodel', 'docid'
table_transaction = {
    "id": "ID",
    "client": "Кліент",
    "datedoc": "Дата",
    "sum": "Сума",
    "balance": "Баланс",
    "docapp": "Модуль",
    "docmodel": "Модель",
    "docid": "ІД",
    "datetime": "Дата",
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

paytypes = { 1: "безготівковий", 2: "готівковий" }
paystatuses = { 1: "проведено", 2: "не проведено" }

# id, num, client, nomenclature, price, orderdate, enddate, pccode, licensecode, seller, 
# developer, devdiscount, devprice, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment
table_license = {
    "id": "ID",
    "num": "Номер",
    "client": "Кліент",
    "nomenclature": "Ліцензія",
    "price": "Ціна",
    "orderdate": "Дата замовлення",
    "enddate": "Дата закінчення",
    "pccode": "Код компьютера",
    "licensecode": "Код ліцензії",
    "seller": "Постачальник",
    "developer": "Розробник",
    "devdiscount": "Відсоток Розробника",
    "devprice": "Оплата Розробнику",
    "agent": "Агент",
    "agdiscount": "Відсоток Агента",
    "agprice": "Оплата Агенту",
    "taxes": "Податки",
    "taxdiscount": "Відсоток Податку",
    "taxprice": "Оплата Податку",
    "comment": "Коментар",
    "pk": "Дії",
}

table_act = {
    "id": "ID",
    "num": "Номер",
    "datedoc": "Дата",
    "client": "Кліент",
    "nomenclature": "Послуга",
    "price": "Ціна",
    # "orderdate": "Дата замовлення",
    # "enddate": "Дата закінчення",
    # "pccode": "Код компьютера",
    # "licensecode": "Код ліцензії",
    "seller": "Постачальник",
    # "developer": "Розробник",
    # "devdiscount": "Відсоток Розробника",
    # "devprice": "Оплата Розробнику",
    "agent": "Агент",
    "agdiscount": "Відсоток Агента",
    "agprice": "Оплата Агенту",
    "taxes": "Податки",
    "taxdiscount": "Відсоток Податку",
    "taxprice": "Оплата Податку",
    "comment": "Коментар",
    "pk": "Дії",
}