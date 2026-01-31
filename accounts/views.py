from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .forms import UserRegisterForm, UserLoginForm

from accounts.libs.adddata import *
from accounts.libs.settings import *


def register(request):
    elems = buttons
    title = msg.get("registar_title")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, msg.get("register_success"))
            return redirect("client_list")
        else:
            messages.error(request, msg.get("register_error"))
    else:
        form = UserRegisterForm()
    return render(
        request,
        "accounts/register.html",
        {"form": form, "title": title, "elems": elems},
    )


def user_login(request):
    elems = buttons
    title = msg.get("login_title")
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, msg.get("login_success"))
            return redirect("client_list")
    else:
        form = UserLoginForm()
    return render(
        request,
        "accounts/login.html",
        {"form": form, "title": title, "elems": elems},
    )


def user_logout(request):
    logout(request)
    return redirect("login")

def user_detail(request):
    item = request.user
    elems = buttons
    title = msg.get("user") + ": " + item.username
    return render(
        request,
        "accounts/user_detail.html",
        {"item": item, "title": title, "elems": elems, "card_titles":user_titles},
    )

