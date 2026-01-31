from django.urls import reverse

site_logo = {"site_name": "Облік клієнтів", "logo_url": reverse("home"), "childs": 0}

menus = [
    {"title": "Головна", "url": reverse("home"), "childs": 0},
    {"title": "Клієнти", "url": reverse("client_list"), "childs": 0},
    {"title": "Контакти", "url": reverse("contact_list"), "childs": 0},
    {"title": "Доступи", "url": reverse("access_list"), "childs": 0},
    # {"title": "Баланс", "url": reverse("balance_list"), "childs": 0},
    {
        "title": "Фінанси",
        "url": "#",
        "childs": [
            {"title": "Баланс", "url": reverse("balance_list"), "childs": 1},
            {"title": "Прайс", "url": reverse("price_list"), "childs": 1},
            {"title": "Знижка", "url": reverse("discount_list"), "childs": 1},
        ],
    },
    {
        "title": "Довідники",
        "url": "#",
        "childs": [
            {"title": "Теги", "url": reverse("tag_list"), "childs": 1},
            {"title": "Номенклатура", "url": reverse("nomenclature_list"), "childs": 1},
            {"title": "Адреси", "url": reverse("fulladdress_list"), "childs": 1},
            {"title": "Міста", "url": reverse("city_list"), "childs": 1},
            {"title": "Райони", "url": reverse("distr_list"), "childs": 1},
            {"title": "Вулиці", "url": reverse("street_list"), "childs": 1},
        ],
    },
    # {
    #     "title": "Adminka",
    #     "url": "#",
    #     "childs": [
    #         {"title": "Logs", "url": reverse("adminka_log_list"), "childs": 6},
    #         # {"title": "Теги", "url": reverse("tags"), "childs": 5},
    #     ],
    # },
]

adms = [
    {
        "title": "Adminka",
        "url": "#",
        "childs": [
            {"title": "Site-Admin", "url": reverse("site-admin"), "childs": 1},
            {"title": "Logs", "url": reverse("islog_list"), "childs": 2},
            # {"title": "Теги", "url": reverse("tags"), "childs": 5},
        ],
    },
]

adm_menus = menus + adms

