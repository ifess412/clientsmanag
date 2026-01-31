from django.urls import path, include
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("user/", user_detail, name="user_detail"),
    # path("user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    # path('', include('django.contrib.auth.urls')),
    # path("", index, name="home"),
    # path("filterbytag/<str:slug>/", FilterByTag.as_view(), name="filterbytag"),
    # path("search/", Search.as_view(), name="search"),
    # path(
    #     "tags/",
    #     include(
    #         [
    #             path("", TagListView.as_view(), name="tag_list"),
    #             path("create/", TagCreateView.as_view(), name="tag_create"),
    #             path("<str:slug>/", TagDetailView.as_view(), name="tag_detail"),
    #             path("<str:slug>/update/", TagUpdateView.as_view(), name="tag_update"),
    #             path("<str:slug>/delete/", TagDeleteView.as_view(), name="tag_delete"),
    #         ]
    #     ),
    # ),
]

# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']