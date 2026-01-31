from django.urls import path, include

from .views import *

urlpatterns = [
    # path("logs/<str:app>/<str:mdl>/<int:id>", IslogListView.as_view(), name="log_list"),
    # path("search/", Search.as_view(), name="search"),
    path(
        "",
        include(
            [
                # path("", TagListView.as_view(), name="tag_list"),
                path("", IslogListView.as_view(), name="islog_list"),
                # path("create/", TagCreateView.as_view(), name="tag_create"),
                # path("<str:slug>/", TagDetailView.as_view(), name="tag_detail"),
                # path("<str:slug>/update/", TagUpdateView.as_view(), name="tag_update"),
                path("<int:pk>/delete/", IslogDeleteView.as_view(), name="islog_delete"),
                path("<str:app>/<str:mdl>/<int:id>", FilterIslogListView.as_view(), name="filter_islog_list"),
            ]
        ),
    ),
]
