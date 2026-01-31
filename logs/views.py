from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
# from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from django.db.models import F
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import PermissionDenied
# from django.contrib.auth.decorators import login_required

from .models import *
# from .forms import NomenclatureForm

from libs.all_adddata import *
from libs.logs_adddata import *
from libs.settings import *

# # for logging
# from .signals import *


APPL = "logs"


def get_last_log(app_label = None, obj_model = None, obj_id = None, action_tag = None):
    filtered_queryset = Islog.objects.filter(app_label=app_label).filter(obj_model=obj_model).filter(obj_id=obj_id).order_by('-date_time').first()
    if (filtered_queryset) : return filtered_queryset
    else: return None

# id, app_label, obj_model, obj_id, mess, action_tag, user_id, date_time
class FilterIslogListView(PermissionRequiredMixin, ListView):
    model = Islog
    mdl = model._meta.model_name
    # mdl_name = model._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    # mdls = "islogs"
    context_object_name = "items"
    template_name = APPL + "/" + mdl + "_filterlist.html"
    paginate_by = paginate_in_tables
    login_url = reverse_lazy('login')
    # permission_required = "logs.view_islog"
    permission_required = APPL + ".view_" + mdl
    # redirect_field_name = 'clients'
    # raise_exception = True

    def get_queryset(self):
        return Islog.objects.filter(app_label=self.kwargs["app"]).filter(obj_model=self.kwargs["mdl"]).filter(obj_id=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
        mdl_name_pl = thismodel._meta.verbose_name_plural
        # mdls = self.mdls
        context["columnames"] = table_logs
        # context["client_type"] = client_type
        context["elems"] = buttons
        context["err_msg"] = msg["no_data_in_db"]
        context["title"] = mdl_name_pl
        context['actions'] = action_tag
        selfapp = self.kwargs["app"]
        selfmodel = self.kwargs["mdl"]
        selfid = self.kwargs["id"]
        # print(selfmodel)
        context["objtitle"] = mdl_name_pl + " for " + str(selfapp) + "/" + str(selfmodel) + ' ID: ' + str(selfid)
        return context

class IslogListView(PermissionRequiredMixin, ListView):
    model = Islog
    mdl = model._meta.model_name
    # mdls = "islogs"
    context_object_name = "items"
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables_adminka
    login_url = reverse_lazy('login')
    # permission_required = ("logs.view_islog", 'logs.delete_islog')
    permission_1 = APPL + ".view_" + mdl
    permission_2 = APPL + ".delete_" + mdl
    permission_required = (permission_1, permission_2)
    # redirect_field_name = 'clients'
    # raise_exception = True

    def get_queryset(self):
        # return Islog.objects.filter(app_label=self.kwargs["app"]).filter(obj_model=self.kwargs["mdl"]).filter(obj_id=self.kwargs["id"])
        # queryset = Islog.objects.all()
        queryset = Islog.objects.order_by('-date_time')
        fapp = self.request.GET.get("fapp")
        if fapp:
            queryset = queryset.filter(
                Q(app_label__icontains=fapp)
                | Q(app_label__icontains=fapp)
                )
        fmodel = self.request.GET.get("fmodel")
        if fmodel:
            queryset = queryset.filter(
                Q(obj_model__icontains=fmodel)
                | Q(obj_model__icontains=fmodel)
                )
        fid = self.request.GET.get("fid")
        if fid:
            queryset = queryset.filter(obj_id=fid)
        ftype = self.request.GET.get("ftype")
        if ftype:
            if ftype == 'add': ftype = 1
            elif ftype == "edit": ftype = 2
            elif ftype == "delete": ftype = 3
            queryset = queryset.filter(action_tag=ftype)
        ftime = self.request.GET.get("ftime")
        if ftime:
            queryset = queryset.filter(date_time__icontains=ftime)
        fuser = self.request.GET.get("fuser")
        if fuser:
            queryset = queryset.filter(
                Q(user__username=fuser)
                | Q(user__first_name=fuser)
                # | Q(user__icontains=fuser)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
        mdl_name_pl = thismodel._meta.verbose_name_plural
        # mdls = "islogs"
        context["columnames"] = table_admlogs
        # context["client_type"] = client_type
        context["elems"] = buttons
        context["err_msg"] = msg["no_data_in_db"]
        # context["count_msg"] = msg["count_text"]
        context["title"] = mdl_name_pl
        context['actions'] = action_tag
        context["this_url"] = reverse_lazy(mdl +"_list")
        context["s"] = ""
        fapp = self.request.GET.get("fapp")
        if fapp:
            context["s"] += f"fapp={fapp}&"
        fmodel = self.request.GET.get("fmodel")
        if fmodel:
            context["s"] += f"fmodel={fmodel}&"
        fid = self.request.GET.get("fid")
        if fid:
            context["s"] += f"fid={fid}&"
        ftype = self.request.GET.get("ftype")
        if ftype:
            context["s"] += f"ftype={ftype}&"
        ftime = self.request.GET.get("ftime")
        if ftime:
            context["s"] += f"ftime={ftime}&"
        fuser = self.request.GET.get("fuser")
        if fuser:
            context["s"] += f"fuser={fuser}&"
            
        # ftime = self.request.GET.get("ftime")
        # if ftime:
        #     context["ftime"] = f"ftime={ftime}&"
        # context["s"] = f"s={search_field}&"
        # selfapp = self.kwargs["app"]
        # selfmodel = self.kwargs["mdl"]
        # context["objtitle"] = mdlnames.get(mdls) + " for " + mdlnames.get(selfmodel) + ' ID: ' + str(self.kwargs["id"])
        return context
    
    # def post(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    #     allow_empty = self.get_allow_empty()

    #     if not allow_empty:
    #         # When pagination is enabled and object_list is a queryset,
    #         # it's better to do a cheap query than to load the unpaginated
    #         # queryset in memory.
    #         if self.get_paginate_by(self.object_list) is not None and hasattr(
    #             self.object_list, "exists"
    #         ):
    #             is_empty = not self.object_list.exists()
    #         else:
    #             is_empty = not self.object_list
    #         if is_empty:
    #             raise Http404(
    #                 _("Empty list and “%(class_name)s.allow_empty” is False.")
    #                 % {
    #                     "class_name": self.__class__.__name__,
    #                 }
    #             )
    #     context = self.get_context_data()
    #     return self.render_to_response(context)
    
class IslogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Islog
    mdl = model._meta.model_name
    # fields = [
    #     "title",
    # ]
    template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    # success_url = reverse_lazy("islog_list")
    permission_required = APPL + ".delete_" + mdl
    # permission_required = "logs.delete_islog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        context["elems"] = buttons
        context["msg"] = msg["del_question"]
        obj_obj = Islog.objects.get(pk=self.kwargs["pk"])
        # print(obj_obj)
        # obj_str = str(obj_obj)
        obj_id = obj_obj.id
        context["title"] = msg.get("del_title") + ' ID ' + str(obj_id)
        # context["back_url"] = reverse_lazy("islog_list")
        context["back_url"] = reverse_lazy(mdl + "_list")
        return context


