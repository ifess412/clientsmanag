from django.urls import path, include
from .views import *

urlpatterns = [
    # path("register/", register, name="register"),
    # path("login/", user_login, name="login"),
    # path("logout/", user_logout, name="logout"),
    # path("user/", user_detail, name="user_detail"),
    # path("user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    # path('', include('django.contrib.auth.urls')),
    # path("", index, name="home"),
    # path("filterbytag/<str:slug>/", FilterByTag.as_view(), name="filterbytag"),
    # path("search/", Search.as_view(), name="search"),
    path(
        "nomenclature/",
        include(
            [
                path("", NomenclatureListView.as_view(), name="nomenclature_list"),
                path("create/", NomenclatureCreateView.as_view(), name="nomenclature_create"),
                path("<str:slug>/", NomenclatureDetailView.as_view(), name="nomenclature_detail"),
                path("<str:slug>/update/", NomenclatureUpdateView.as_view(), name="nomenclature_update"),
                path("<str:slug>/delete/", NomenclatureDeleteView.as_view(), name="nomenclature_delete"),
            ]
        ),
    ),
    path(
        "price/",
        include(
            [
                path("", PriceListView.as_view(), name="price_list"),
                path("add/", PriceCreateItem, name="price_add"),
                path("create/", PriceCreateView.as_view(), name="price_create"),
                path("<int:pk>/", PriceDetailView.as_view(), name="price_detail"),
                path("<int:pk>/update/", PriceUpdateView.as_view(), name="price_update"),
                path("<int:pk>/delete/", PriceDeleteView.as_view(), name="price_delete"),
            ]
        ),
    ),
    path(
        "discount/",
        include(
            [
                path("", DiscountListView.as_view(), name="discount_list"),
                path("add/", DiscountCreateItem, name="discount_add"),
                path("create/", DiscountCreateView.as_view(), name="discount_create"),
                path("<int:pk>/", DiscountDetailView.as_view(), name="discount_detail"),
                path("<int:pk>/update/", DiscountUpdateView.as_view(), name="discount_update"),
                path("<int:pk>/delete/", DiscountDeleteView.as_view(), name="discount_delete"),
            ]
        ),
    ),
    path(
        "cashbook/",
        include(
            [
                path("", CashbookListView.as_view(), name="cashbook_list"),
                path("create/", CashbookCreateView.as_view(), name="cashbook_create"),
                path("<int:pk>/", CashbookDetailView.as_view(), name="cashbook_detail"),
                path("<int:pk>/update/", CashbookUpdateView.as_view(), name="cashbook_update"),
                path("<int:pk>/delete/", CashbookDeleteView.as_view(), name="cashbook_delete"),
            ]
        ),
    ),
    path(
        "balance/",
        include(
            [
                path("", BalanceListView.as_view(), name="balance_list"),
                path("add/", BalanceCreateItem, name="balance_add"),
                path("create/", BalanceCreateView.as_view(), name="balance_create"),
                path("<int:pk>/", BalanceDetailView.as_view(), name="balance_detail"),
                path("<int:pk>/update/", BalanceUpdateView.as_view(), name="balance_update"),
                path("<int:pk>/delete/", BalanceDeleteView.as_view(), name="balance_delete"),
            ]
        ),
    ),
    path(
        "transaction/",
        include(
            [
                path("", TransactionListView.as_view(), name="transaction_list"),
                # path("create/", CashbookCreateView.as_view(), name="cashbook_create"),
                # path("<int:pk>/", CashbookDetailView.as_view(), name="cashbook_detail"),
                # path("<int:pk>/update/", CashbookUpdateView.as_view(), name="cashbook_update"),
                path("<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
                # path("<str:app>/<str:mdl>/<int:id>", TransactionFilteredListView.as_view(), name="transaction_filtered_list"),
            ]
        ),
    ),
    path(
        "license/",
        include(
            [
                path("", LicenseListView.as_view(), name="license_list"),
                path("create/", LicenseCreateView.as_view(), name="license_create"),
                path("<int:pk>/", LicenseDetailView.as_view(), name="license_detail"),
                path("<int:pk>/update/", LicenseUpdateView.as_view(), name="license_update"),
                path("<int:pk>/delete/", LicenseDeleteView.as_view(), name="license_delete"),
            ]
        ),
    ),
    path(
        "act/",
        include(
            [
                path("", ActListView.as_view(), name="act_list"),
                path("create/", ActCreateView.as_view(), name="act_create"),
                path("<int:pk>/", ActDetailView.as_view(), name="act_detail"),
                path("<int:pk>/update/", ActUpdateView.as_view(), name="act_update"),
                path("<int:pk>/delete/", ActDeleteView.as_view(), name="act_delete"),
            ]
        ),
    ),
    path('ajax/get-price/', get_lic_price_json, name='get_lic_price'),
    path('ajax/get-discount/', get_discount_json, name='get_discount'),
    path('ajax/get-next-doc-number/', get_next_doc_number, name='get_next_doc_number'),
    # path('finances/ajax/get-next-doc-number/', views.get_next_doc_number, name='get_next_doc_number'),
]

# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']