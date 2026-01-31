from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from accounts.libs.adddata import msg


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=msg.get("username"),
        # label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label=msg.get("password1"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label=msg.get("username"),
        help_text=msg.get("username_help"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label=msg.get("password1"),
        help_text=msg.get("password1_help"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label=msg.get("password2"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        max_length=250,
        label=msg.get("email"), 
        help_text=msg.get("email_help"), 
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        label=msg.get("first_name"),
        # help_text=msg.get("username_help"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label=msg.get("last_name"),
        # help_text=msg.get("username_help"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(
#         label=msg.get("form_username"),
#         help_text="Максимум 150 символів",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )
#     password1 = forms.CharField(
#         label=msg.get("form_pass1"),
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#     )
#     password2 = forms.CharField(
#         label=msg.get("form_pass2"),
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#     )
#     email = forms.EmailField(
#         label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"})
#     )

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
#         labels = {
#             "username": ("Writer"),
#         }
#         help_texts = {
#             "username": ("Some useful help text."),
#         }
#         error_messages = {
#             "username": {
#                 "max_length": ("This writer's name is too long."),
#             },
#         }
#         widgets = {
#             "username": forms.TextInput(attrs={"class": "form-control"}),
#         }
