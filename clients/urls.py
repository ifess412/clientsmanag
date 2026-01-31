from django.urls import path, re_path, include

from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("/admin", redirect_to_external_site, name="site-admin"),
    path("filterbytag/<str:slug>/", FilterByTag.as_view(), name="filterbytag"),
    # path("export/", clients_export_to_excel,{'model':'client','orderby': 'pk', 'filterby':''}, name="export_to_excel"),
    # path("export/<str:model>/", clients_export_to_excel, {'orderby': 'pk', 'filterby':''} , name="export_to_excel"),
    # path("export/<str:model>/<str:orderby>/", clients_export_to_excel,{'filterby':''}, name="export_to_excel"),
    # path("export/<str:model>/<str:orderby>/<str:filterby>/", clients_export_to_excel, name="export_to_excel"),
    # re_path(r'^export/(?P<model>\d+)?$', clients_export_to_excel, name='export_to_excel'),
    path(
        "export/",
        include(
            [
                path("", clients_export_to_excel,{'model':'client','orderby': 'pk', 'filterrows':''}, name="export_to_excel"),
                path("<str:model>/", clients_export_to_excel, {'orderby': 'pk', 'filterrows':''} , name="export_to_excel"),
                path("<str:model>/<str:orderby>/", clients_export_to_excel,{'filterrows':''}, name="export_to_excel"),
                path("<str:model>/<str:orderby>/<str:filterrows>/", clients_export_to_excel, name="export_to_excel"),
            ]
        ),
    ),

    # path("logs/<str:app>/<str:mdl>/<int:id>", IslogListView.as_view(), name="log_list"),
    # # path("search/", Search.as_view(), name="search"),
    # path(
    #     "adminka/",
    #     include(
    #         [
    #             # path("", TagListView.as_view(), name="tag_list"),
    #             path("logs/", AdminkaIslogListView.as_view(), name="adminka_log_list"),
    #             # path("create/", TagCreateView.as_view(), name="tag_create"),
    #             # path("<str:slug>/", TagDetailView.as_view(), name="tag_detail"),
    #             # path("<str:slug>/update/", TagUpdateView.as_view(), name="tag_update"),
    #             path("logs/<int:pk>/delete/", IslogDeleteView.as_view(), name="islog_delete"),
    #         ]
    #     ),
    # ),
    path(
        "tags/",
        include(
            [
                path("", TagListView.as_view(), name="tag_list"),
                path("create/", TagCreateView.as_view(), name="tag_create"),
                path("<str:slug>/", TagDetailView.as_view(), name="tag_detail"),
                path("<str:slug>/update/", TagUpdateView.as_view(), name="tag_update"),
                path("<str:slug>/delete/", TagDeleteView.as_view(), name="tag_delete"),
            ]
        ),
    ),
    path(
        "access/",
        include(
            [
                path("", AccessListView.as_view(), name="access_list"),
                path("create/", AccessCreateView.as_view(), name="access_create"),
                path("<str:slug>/", AccessDetailView.as_view(), name="access_detail"),
                path("<str:slug>/update/", AccessUpdateView.as_view(), name="access_update"),
                path("<str:slug>/delete/", AccessDeleteView.as_view(), name="access_delete"),
                path("filter/<str:slug>/", AccessListView.as_view(), name="access_list_by_client"),
            ]
        ),
    ),
    path(
        "contacts/",
        include(
            [
                path("", ContactListView.as_view(), name="contact_list"),
                path("create/", ContactCreateView.as_view(), name="contact_create"),
                path("<str:slug>/", ContactDetailView.as_view(), name="contact_detail"),
                path("<str:slug>/update/", ContactUpdateView.as_view(), name="contact_update"),
                path("<str:slug>/delete/", ContactDeleteView.as_view(), name="contact_delete"),
            ]
        ),
    ),
    path(
        "clients/",
        include(
            [
                path("", ClientListView.as_view(), name="client_list"),
                path("create/", ClientCreateView.as_view(), name="client_create"),
                path("<str:slug>/", ClientDetailView.as_view(), name="client_detail"),
                path("<str:slug>/update/", ClientUpdateView.as_view(), name="client_update"),
                path("<str:slug>/delete/", ClientDeleteView.as_view(), name="client_delete"),
            ]
        ),
    ),
    path(
        "cities/",
        include(
            [
                path("", CityListView.as_view(), name="city_list"),
                path("create/", CityCreateView.as_view(), name="city_create"),
                path("<str:slug>/", CityDetailView.as_view(), name="city_detail"),
                path("<str:slug>/update/", CityUpdateView.as_view(), name="city_update"),
                path("<str:slug>/delete/", CityDeleteView.as_view(), name="city_delete"),
            ]
        ),
    ),
    path(
        "distr/",
        include(
            [
                path("", DistrListView.as_view(), name="distr_list"),
                path("create/", DistrCreateView.as_view(), name="distr_create"),
                path("<int:pk>/", DistrDetailView.as_view(), name="distr_detail"),
                path("<int:pk>/update/", DistrUpdateView.as_view(), name="distr_update"),
                path("<int:pk>/delete/", DistrDeleteView.as_view(), name="distr_delete"),
            ]
        ),
    ),
    path(
        "street/",
        include(
            [
                path("", StreetListView.as_view(), name="street_list"),
                path("create/", StreetCreateView.as_view(), name="street_create"),
                path("<int:pk>/", StreetDetailView.as_view(), name="street_detail"),
                path("<int:pk>/update/", StreetUpdateView.as_view(), name="street_update"),
                path("<int:pk>/delete/", StreetDeleteView.as_view(), name="street_delete"),
            ]
        ),
    ),
    path(
        "fulladdress/",
        include(
            [
                path("", FulladdressListView.as_view(), name="fulladdress_list"),
                path("create/", FulladdressCreateView.as_view(), name="fulladdress_create"),
                path("<int:pk>/", FulladdressDetailView.as_view(), name="fulladdress_detail"),
                path("<int:pk>/update/", FulladdressUpdateView.as_view(), name="fulladdress_update"),
                path("<int:pk>/delete/", FulladdressDeleteView.as_view(), name="fulladdress_delete"),
            ]
        ),
    ),



]
