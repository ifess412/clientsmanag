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
        "balance/",
        include(
            [
                path("", BalanceListView.as_view(), name="balance_list"),
                path("create/", PriceCreateView.as_view(), name="balance_create"),
                path("<int:pk>/", PriceDetailView.as_view(), name="balance_detail"),
                path("<int:pk>/update/", PriceUpdateView.as_view(), name="balance_update"),
                path("<int:pk>/delete/", PriceDeleteView.as_view(), name="balance_delete"),
            ]
        ),
    ),
]

# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']