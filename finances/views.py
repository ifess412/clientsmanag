# from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# # from django.db.models import F
from django.db.models import Q
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# # from django.core.exceptions import PermissionDenied
# # from django.contrib.auth.decorators import login_required


from .models import *
from .forms import NomenclatureForm, PriceForm, DiscountForm

# Додаткові дані та налаштування
from libs.all_adddata import *
from libs.finances_adddata import *
from libs.settings import *
from libs.add_func import *

# # for logging
# from .signals import *
# signals imported in app
from logs.views import get_last_log

APPL = "finances"

# def checkSlugField(model):
#     column_names = [field.name for field in model._meta.get_fields() if hasattr(field, 'name')]
#     slugfield = False
#     checkname = 'slug'
#     if checkname in column_names:
#         slugfield = True
#     else:
#         slugfield = False
#     return slugfield

# def getOneObj(model, instance, params=False):
#     sf = checkSlugField(model)
#     if sf :
#         obj_obj = model.objects.get(slug=instance.kwargs["slug"])
#     else : 
#         obj_obj = model.objects.get(pk=instance.kwargs["pk"])
#     return obj_obj

class MyListView(PermissionRequiredMixin, ListView):
    # 
    model = Nomenclature
    mdl = model._meta.model_name
    # mdl_name = model._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    context_object_name = "items"
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables_finance
    permission_required = APPL + ".view_" + mdl
    columnames = table_nomenclature
    show_colums = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    sort_fields = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    # search_in_fields = ['name__icontains', 'name__icontains']

    def get_queryset(self):
        thismodel = self.model
        queryset = thismodel.objects.all()
        filter_by_client = self.request.GET.get("f")
        if filter_by_client:
            queryset = queryset.order_by('order').filter(
                Q(client__slug=filter_by_client)
                # | Q(app_label__icontains=fapp)
                )
        sort_by = self.request.GET.get("sort")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        # mdl_name = thismodel._meta.verbose_name
        mdl_name_pl = thismodel._meta.verbose_name_plural
        context["sort_fields"] = self.sort_fields
        context["show_colums"] = self.show_colums
        context["columnames"] = self.columnames
        context["elems"] = buttons
        context["err_msg"] = msg["no_data_in_db"]
        context["new_url"] = reverse_lazy(mdl +"_create")
        context["this_url"] = reverse_lazy(mdl +"_list")
        context["add_url"] = mdl +"_add"
        context["dtl_url"] = mdl +"_detail"
        context["upd_url"] = mdl +"_update"
        context["del_url"] = mdl +"_delete"
        context["title"] = mdl_name_pl
        search_field = self.request.GET.get("s")
        if search_field:
            context["s"] = f"s={search_field}&"
            context["title"] = mdl_name_pl + msg.get('search_title') + str(search_field)
        filter_by_client = self.request.GET.get("f")
        if filter_by_client:
            context["s"] = f"s={search_field}&"
            context["title"] = mdl_name_pl + msg.get('filter_title') + str(filter_by_client)
        sort_by = self.request.GET.get("sort")
        if sort_by:
            context["s"] = f"sort={sort_by}&"
        return context
    
class MyDetailView(PermissionRequiredMixin, DetailView):
    model = Nomenclature
    mdl = model._meta.model_name
    # mdl_name = thismodel._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    context_object_name = "item"
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_nomenclature

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
        # mdl_name_pl = thismodel._meta.verbose_name_plural
        context["card_titles"] = self.card_titles
        context["elems"] = buttons
        # obj_obj = thismodel.objects.get(slug=self.kwargs["slug"])
        obj_obj = getOneObj(thismodel, self)
        obj_str = str(obj_obj)
        obj_id = obj_obj.id
        context["title"] = (mdl_name + ": " + obj_str)
        context["back_url"] = reverse_lazy(mdl +"_list")
        lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
        if (lastupd) :
            context["lastupd"] = lastupd.date_time
            context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
        return context

class MyCreateView(PermissionRequiredMixin, CreateView):
    # form_class = TagForm
    model = Nomenclature
    mdl = model._meta.model_name
    # mdl_name = thismodel._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    # mdl = "tag"
    context_object_name = "item"
    template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
        mdl_name_pl = thismodel._meta.verbose_name_plural
        context["elems"] = buttons
        context["title"] = msg.get("add") + mdl_name
        context["back_url"] = reverse_lazy(mdl +"_list")
        return context

class MyUpdateView(PermissionRequiredMixin, UpdateView):
    # form_class = AccessForm
    model = Nomenclature
    mdl = model._meta.model_name
    # fields = ["title", "color"]
    context_object_name = "item"
    template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_nomenclature

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
        mdl_name_pl = thismodel._meta.verbose_name_plural
        context["card_titles"] = self.card_titles
        context["elems"] = buttons
        context["title"] = msg.get("edit") + mdl_name
        context["back_url"] = reverse_lazy(mdl + "_list")
        return context

class MyDeleteView(PermissionRequiredMixin, DeleteView):
    model = Nomenclature
    mdl = model._meta.model_name
    # fields = [
    #     "title",
    # ]
    template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    # success_url = reverse_lazy("nomenclature_list")
    permission_required = APPL + ".delete_" + mdl

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        # mdl_name = thismodel._meta.verbose_name
        # mdl_name_pl = thismodel._meta.verbose_name_plural
        context["elems"] = buttons
        context["msg"] = msg["del_question"]
        context["title"] = msg.get("del_title")
        context["back_url"] = reverse_lazy(mdl + "_list")
        # context["back_url"] = reverse_lazy("nomenclature_list")
        return context

class NomenclatureListView(MyListView):
    # id, name, fullname, code, address, comment, type, tags, slug
    model = Nomenclature
    mdl = model._meta.model_name
    # mdls = "clients"
    # mdl = "client"
    template_name = APPL + "/" + mdl + "_list.html"
    # paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_nomenclature
    show_colums = ['id', 'name', 'fullname', 'code', 'type', 'tag', 'pk']
    sort_fields = ['id', 'name', 'fullname', 'code', 'type', 'tag']
    # client_type = client_type

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field) 
                | Q(name__icontains=search_field2)
                | Q(fullname__icontains=search_field)
                | Q(code__icontains=search_field)
                )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nomenclature_type"] = nomenclature_type
        return context

class NomenclatureDetailView(MyDetailView):
    model = Nomenclature
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_nomenclature

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nomenclature_type"] = nomenclature_type
        return context

class NomenclatureCreateView(MyCreateView):
    form_class = NomenclatureForm
    model = Nomenclature
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class NomenclatureUpdateView(MyUpdateView):
    form_class = NomenclatureForm
    model = Nomenclature
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_nomenclature

class NomenclatureDeleteView(MyDeleteView):
    model = Nomenclature
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

def PriceCreateItem(request):
    model = Price
    mdl = model._meta.model_name
    # mdl = "price"
    search_field = request.GET.get("i")
    if search_field:
        N1 = Nomenclature.objects.get(name=search_field)
        new=Price.objects.create(nomenclature=N1, price=0)
        return redirect(mdl +"_update", pk=new.pk)
    else: return redirect(mdl +"_create")

class PriceListView(MyListView):
    # id, nomenclature, price, datetime
    model = Price
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_price
    show_colums = ['id','code', 'name', 'fullname', 'prices__price', 'prices__datetime', 'pk']
    sort_fields = ['id','code', 'name', 'fullname', 'prices__price', 'prices__datetime']

    def get_queryset(self):
        # queryset = super().get_queryset()
        queryset = Nomenclature.objects.values('pk','code', 'name', 'prices__pk', 'prices__price', 'prices__datetime')
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field)
                | Q(name__icontains=search_field2)
                | Q(fullname__icontains=search_field)
                | Q(code__icontains=search_field)
            )
        sort_by = self.request.GET.get("sort")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["nomenclature_type"] = nomenclature_type
        return context

class PriceDetailView(MyDetailView):
    model = Price
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["nomenclature_type"] = nomenclature_type
        return context

class PriceCreateView(MyCreateView):
    form_class = PriceForm
    model = Price
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class PriceUpdateView(MyUpdateView):
    form_class = PriceForm
    model = Price
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_price

class PriceDeleteView(MyDeleteView):
    model = Price
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

def DiscountCreateItem(request):
    model = Discount
    mdl = model._meta.model_name
    search_field = request.GET.get("i")
    if search_field:
        C1 = Client.objects.get(name=search_field)
        new = Discount.objects.create(client=C1, discount=0)
        return redirect(mdl +"_update", pk=new.pk)
    else: return redirect(mdl +"_create")

class DiscountListView(MyListView):
    #  name, fullname, code
    model = Discount
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_discount
    show_colums = ['id', 'code','name', 'fullname', 'discount__discount', 'discount__datetime', 'pk']
    sort_fields = ['id', 'code','name', 'fullname', 'discount__discount', 'discount__datetime']

    def get_queryset(self):
        # name, fullname, code
        queryset = Client.objects.values('pk', 'code', 'name', 'fullname', 'discount__pk', 'discount__discount', 'discount__datetime')
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field)
                | Q(name__icontains=search_field2)
                | Q(fullname__icontains=search_field)
                | Q(code__icontains=search_field)
            )
        sort_by = self.request.GET.get("sort")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["nomenclature_type"] = nomenclature_type
        return context

class DiscountDetailView(MyDetailView):
    model = Discount
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_discount

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["nomenclature_type"] = nomenclature_type
        return context

class DiscountCreateView(MyCreateView):
    form_class = DiscountForm
    model = Discount
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class DiscountUpdateView(MyUpdateView):
    form_class = DiscountForm
    model = Discount
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_discount

class DiscountDeleteView(MyDeleteView):
    model = Discount
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class BalanceListView(MyListView):
    #  name, fullname, code
    model = Balance
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_balance
    show_colums = ['id','nomenclature__code', 'nomenclature', 'price', 'date_time', 'pk']
    sort_fields = ['id','nomenclature__code', 'nomenclature', 'price', 'date_time']

    def get_queryset(self):
        # name, fullname, code
        queryset = super().get_queryset()
        # queryset = Client.objects.values('pk', 'code', 'name', 'fullname', 'discount__pk', 'discount__discount', 'discount__datetime')
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(client__name__icontains=search_field)
                | Q(client__name__icontains=search_field2)
                | Q(client__fullname__icontains=search_field)
                # | Q(client__code__icontains=search_field)
            )
        sort_by = self.request.GET.get("sort")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["nomenclature_type"] = nomenclature_type
        return context



# class NomenclatureListView(PermissionRequiredMixin, ListView):
#     model = Nomenclature
#     # APPL = "finances"
#     mdl = "nomenclature"
#     context_object_name = "items"
#     template_name = APPL + "/" + mdl + "_list.html"
#     paginate_by = paginate_in_tables_finance
#     login_url = reverse_lazy('login')
#     # permission_required = "finances.view_nomenclature"
#     permission_required = APPL + ".view_" + mdl
#     sort_fields = ['id', 'name', 'fullname', 'code', 'type', 'tag']
#     # redirect_field_name = 'contact_list'
#     # raise_exception = True

#     def get_queryset(self):
#         queryset = Nomenclature.objects.all()
#         search_field = self.request.GET.get("s")
#         if search_field:
#             search_field2 = search_field.capitalize()
#             queryset = queryset.filter(
#                 Q(name__icontains=search_field)
#                 | Q(name__icontains=search_field2)
#                 | Q(fullname__icontains=search_field)
#                 | Q(code__icontains=search_field)
#             )
#         filter_by_tag = self.request.GET.get("f")
#         if filter_by_tag:
#             queryset = queryset.order_by('order').filter(
#                 Q(client__slug=filter_by_tag)
#                 # | Q(app_label__icontains=fapp)
#                 )
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             queryset = queryset.order_by(sort_by)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["columnames"] = table_nomenclature
#         context["sort_fields"] = self.sort_fields
#         context["nomenclature_type"] = nomenclature_type
#         context["elems"] = buttons
#         context["err_msg"] = msg["no_data_in_db"]
#         context["new_url"] = reverse_lazy(mdl +"_create")
#         context["this_url"] = reverse_lazy(mdl +"_list")
#         context["add_url"] = mdl +"_add"
#         context["dtl_url"] = mdl +"_detail"
#         context["upd_url"] = mdl +"_update"
#         context["del_url"] = mdl +"_delete"
#         context["title"] = mdlnames.get(mdl)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('search_title') + str(search_field)
#         filter_by_client = self.request.GET.get("f")
#         if filter_by_client:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('filter_title') + str(filter_by_client)
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             context["s"] = f"sort={sort_by}&"
#         return context
    
# class NomenclatureDetailView(PermissionRequiredMixin, DetailView):
#     model = Nomenclature
#     mdl = "nomenclature"
#     context_object_name = "item"
#     template_name = APPL + "/" + mdl + "_detail.html"
#     # permission_required = "finances.view_nomenclature"
#     permission_required = APPL + ".view_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["card_titles"] = table_nomenclature
#         context["nomenclature_type"] = nomenclature_type
#         context["elems"] = buttons
#         # mdls = "nomenclature"
#         obj_obj = Nomenclature.objects.get(slug=self.kwargs["slug"])
#         obj_str = str(obj_obj)
#         obj_id = obj_obj.id
#         context["title"] = (mdlnames.get(mdl) + ": " + obj_str)
#         # context["back_url"] = reverse_lazy("nomenclature_list")
#         context["back_url"] = reverse_lazy(mdl +"_list")

#         lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
#         if (lastupd) :
#             context["lastupd"] = lastupd.date_time
#             context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
#         print(lastupd)
#         return context

# class NomenclatureCreateView(PermissionRequiredMixin, CreateView):
#     form_class = NomenclatureForm
#     mdl = "nomenclature"
#     # model = Contact
#     # fields = [
#     #     "name",
#     #     "phone1",
#     #     "phone2",
#     #     "phone3",
#     #     "email",
#     #     "client",
#     #     "position",
#     #     "order",
#     #     "comment",
#     # ]
#     # APPL = "finances"
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl +"_list")
#     permission_required = APPL + ".add_" + mdl
#     # permission_required = "finances.add_nomenclature"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         # context["card_titles"] = table_contacts
#         context["elems"] = buttons
#         # mdls = "nomenclature"
#         context["title"] = msg.get("add") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl +"_list")
#         return context

# class NomenclatureUpdateView(PermissionRequiredMixin, UpdateView):
#     form_class = NomenclatureForm
#     model = Nomenclature
#     mdl = "nomenclature"
#     # fields = [
#     #     "name",
#     #     "phone1",
#     #     "phone2",
#     #     "phone3",
#     #     "email",
#     #     "client",
#     #     "position",
#     #     "order",
#     #     "comment",
#     #     # "slug",
#     # ]
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl + "_list")
#     permission_required = APPL + ".change_" + mdl
#     # permission_required = "finances.change_nomenclature"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         # mdls = "nomenclature"
#         context["card_titles"] = table_nomenclature
#         context["elems"] = buttons
#         context["title"] = msg.get("edit") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         return context

# class NomenclatureDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Nomenclature
#     mdl = "nomenclature"
#     fields = [
#         "name",
#     ]
#     template_name = APPL + "/single_delete.html"
#     success_url = reverse_lazy(mdl + "_list")
#     # success_url = reverse_lazy("nomenclature_list")
#     permission_required = APPL + ".delete_" + mdl
#     # permission_required = "finances.delete_nomenclature"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["elems"] = buttons
#         context["msg"] = msg["del_question"]
#         context["title"] = msg.get("del_title")
#         mdl = self.mdl
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         # context["back_url"] = reverse_lazy("nomenclature_list")
#         return context
    
# class PriceListView(PermissionRequiredMixin, ListView):
#     # id, nomenclature, price, datetime
#     model = Price
#     # APPL = "finances"
#     mdl = "price"
#     context_object_name = "items"
#     template_name = APPL + "/" + mdl + "_list.html"
#     paginate_by = paginate_in_tables_finance
#     login_url = reverse_lazy('login')
#     permission_required = APPL + ".view_" + mdl
#     sort_fields = ['id','code', 'name', 'fullname', 'prices__price', 'prices__datetime']
#     # redirect_field_name = 'contact_list'
#     # raise_exception = True

#     def get_queryset(self):
#         # name, fullname, code
#         queryset = Nomenclature.objects.values('pk','code', 'name', 'prices__pk', 'prices__price', 'prices__datetime')
#         # print(queryset)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             search_field2 = search_field.capitalize()
#             queryset = queryset.filter(
#                 Q(name__icontains=search_field)
#                 | Q(name__icontains=search_field2)
#                 | Q(fullname__icontains=search_field)
#                 | Q(code__icontains=search_field)
#             )
#         # or
#         # queryset = Price.objects.all()
#         # search_field = self.request.GET.get("s")
#         # if search_field:
#         #     search_field2 = search_field.capitalize()
#         #     queryset = queryset.filter(
#         #         Q(nomenclature__name__icontains=search_field)
#         #         | Q(nomenclature__name__icontains=search_field2)
#         #         | Q(nomenclature__fullname__icontains=search_field)
#         #         | Q(nomenclature__code__icontains=search_field)
#         #     )
#         filter_by_tag = self.request.GET.get("f")
#         if filter_by_tag:
#             queryset = queryset.order_by('order').filter(
#                 Q(client__slug=filter_by_tag)
#                 # | Q(app_label__icontains=fapp)
#                 )
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             queryset = queryset.order_by(sort_by)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["columnames"] = table_price
#         context["sort_fields"] = self.sort_fields
#         # context["nomenclature_type"] = nomenclature_type
#         context["elems"] = buttons
#         context["err_msg"] = msg["no_data_in_db"]
#         context["new_url"] = reverse_lazy(mdl +"_create")
#         context["this_url"] = reverse_lazy(mdl +"_list")
#         # context["new_url"] = mdl +"_create"
#         context["add_url"] = mdl +"_add"
#         context["upd_url"] = mdl +"_update"
#         context["del_url"] = mdl +"_delete"
#         context["title"] = mdlnames.get(mdl)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('search_title') + str(search_field)
#         filter_by_client = self.request.GET.get("f")
#         if filter_by_client:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('filter_title') + str(filter_by_client)
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             context["s"] = f"sort={sort_by}&"
#         return context
    
# class PriceDetailView(PermissionRequiredMixin, DetailView):
#     model = Price
#     mdl = "price"
#     context_object_name = "item"
#     template_name = APPL + "/" + mdl + "_detail.html"
#     permission_required = APPL + ".view_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["card_titles"] = table_price
#         # context["nomenclature_type"] = nomenclature_type
#         context["elems"] = buttons
#         mdl = self.mdl
#         obj_obj = Price.objects.get(pk=self.kwargs["pk"])
#         obj_str = str(obj_obj)
#         obj_id = obj_obj.id
#         context["title"] = (mdlnames.get(mdl) + ": " + obj_str)
#         context["back_url"] = reverse_lazy(mdl +"_list")
#         lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
#         if (lastupd) :
#             context["lastupd"] = lastupd.date_time
#             context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
#         # print(lastupd)
#         return context


# class PriceCreateView(PermissionRequiredMixin, CreateView):
#     form_class = PriceForm
#     # model = Contact
#     # fields = [
#     #     "name",
#     # ]
#     mdl = "price"
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl +"_list")
#     permission_required = APPL + ".add_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context["card_titles"] = table_contacts
#         context["elems"] = buttons
#         mdl = self.mdl
#         context["title"] = msg.get("add") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl +"_list")
#         return context

# class PriceUpdateView(PermissionRequiredMixin, UpdateView):
#     form_class = PriceForm
#     model = Price
#     mdl = "price"
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl + "_list")
#     permission_required = APPL + ".change_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["card_titles"] = table_price
#         context["elems"] = buttons
#         context["title"] = msg.get("edit") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         return context

# class PriceDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Price
#     fields = [
#         "pk",
#     ]
#     mdl = "price"
#     template_name = APPL + "/single_delete.html"
#     success_url = reverse_lazy(mdl + "_list")
#     permission_required = APPL + ".delete_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["elems"] = buttons
#         context["msg"] = msg["del_question"]
#         context["title"] = msg.get("del_title")
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         return context

# class DiscountListView(PermissionRequiredMixin, ListView):
#     model = Discount
#     # APPL = "finances"
#     mdl = "discount"
#     context_object_name = "items"
#     template_name = APPL + "/" + mdl + "_list.html"
#     paginate_by = paginate_in_tables_finance
#     login_url = reverse_lazy('login')
#     permission_required = APPL + ".view_" + mdl
#     sort_fields = ['id', 'code','name', 'fullname', 'discount__discount', 'discount__datetime']
#     # redirect_field_name = 'contact_list'
#     # raise_exception = True

#     def get_queryset(self):
#         # name, fullname, code
#         queryset = Client.objects.values('pk', 'code', 'name', 'fullname', 'discount__pk', 'discount__discount', 'discount__datetime')
#         # print(queryset)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             search_field2 = search_field.capitalize()
#             queryset = queryset.filter(
#                 Q(name__icontains=search_field)
#                 | Q(name__icontains=search_field2)
#                 | Q(fullname__icontains=search_field)
#                 | Q(code__icontains=search_field)
#             )
#         # or
#         # queryset = Price.objects.all()
#         # search_field = self.request.GET.get("s")
#         # if search_field:
#         #     search_field2 = search_field.capitalize()
#         #     queryset = queryset.filter(
#         #         Q(nomenclature__name__icontains=search_field)
#         #         | Q(nomenclature__name__icontains=search_field2)
#         #         | Q(nomenclature__fullname__icontains=search_field)
#         #         | Q(nomenclature__code__icontains=search_field)
#         #     )
#         filter_by_tag = self.request.GET.get("f")
#         if filter_by_tag:
#             queryset = queryset.order_by('order').filter(
#                 Q(client__slug=filter_by_tag)
#                 # | Q(app_label__icontains=fapp)
#                 )
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             queryset = queryset.order_by(sort_by)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["columnames"] = table_discount
#         context["sort_fields"] = self.sort_fields
#         # context["nomenclature_type"] = nomenclature_type
#         context["elems"] = buttons
#         context["err_msg"] = msg["no_data_in_db"]
#         context["new_url"] = reverse_lazy(mdl +"_create")
#         context["this_url"] = reverse_lazy(mdl +"_list")
#         context["add_url"] = mdl +"_add"
#         context["upd_url"] = mdl +"_update"
#         context["del_url"] = mdl +"_delete"
#         context["title"] = mdlnames.get(mdl)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('search_title') + str(search_field)
#         filter_by_client = self.request.GET.get("f")
#         if filter_by_client:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('filter_title') + str(filter_by_client)
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             context["s"] = f"sort={sort_by}&"
#         return context
    
# class DiscountDetailView(PermissionRequiredMixin, DetailView):
#     pass
#     # model = Price
#     # mdl = "price"
#     # context_object_name = "item"
#     # template_name = APPL + "/" + mdl + "_detail.html"
#     # permission_required = APPL + ".view_" + mdl

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context["card_titles"] = table_price
#     #     # context["nomenclature_type"] = nomenclature_type
#     #     context["elems"] = buttons
#     #     mdl = self.mdl
#     #     obj_obj = Price.objects.get(pk=self.kwargs["pk"])
#     #     obj_str = str(obj_obj)
#     #     obj_id = obj_obj.id
#     #     context["title"] = (mdlnames.get(mdl) + ": " + obj_str)
#     #     context["back_url"] = reverse_lazy(mdl +"_list")
#     #     lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
#     #     if (lastupd) :
#     #         context["lastupd"] = lastupd.date_time
#     #         context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
#     #     # print(lastupd)
#     #     return context

# def DiscountCreateItem(request):
#     mdl = "discount"
#     search_field = request.GET.get("i")
#     if search_field:
#         C1 = Client.objects.get(name=search_field)
#         new=Discount.objects.create(client=C1, discount=0)
#         return redirect(mdl +"_update", pk=new.pk)
#     else: return redirect(mdl +"_create")

# class DiscountCreateView(PermissionRequiredMixin, CreateView):
#     form_class = DiscountForm
#     # model = Contact
#     # fields = [
#     #     "name",
#     # ]
#     mdl = "discount"
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl +"_list")
#     permission_required = APPL + ".add_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context["card_titles"] = table_contacts
#         context["elems"] = buttons
#         mdl = self.mdl
#         context["title"] = msg.get("add") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl +"_list")
#         return context

# class DiscountUpdateView(PermissionRequiredMixin, UpdateView):
#     form_class = DiscountForm
#     model = Discount
#     mdl = "discount"
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl + "_list")
#     permission_required = APPL + ".change_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["card_titles"] = table_discount
#         context["elems"] = buttons
#         context["title"] = msg.get("edit") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         return context

# class DiscountDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Discount
#     fields = [
#         "pk",
#     ]
#     mdl = "discount"
#     template_name = APPL + "/single_delete.html"
#     success_url = reverse_lazy(mdl + "_list")
#     permission_required = APPL + ".delete_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["elems"] = buttons
#         context["msg"] = msg["del_question"]
#         context["title"] = msg.get("del_title")
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         return context

    
# class BalanceListView(PermissionRequiredMixin, ListView):
    model = Balance
    mdl = "balance"
    context_object_name = "items"
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables_finance
    login_url = reverse_lazy('login')
    permission_required = APPL + ".view_" + mdl
    sort_fields = ['id','nomenclature__code', 'nomenclature', 'price', 'date_time']
    # redirect_field_name = 'contact_list'
    # raise_exception = True

    def get_queryset(self):
        queryset = Balance.objects.all()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(client__name__icontains=search_field)
                | Q(client__name__icontains=search_field2)
                | Q(client__fullname__icontains=search_field)
                # | Q(client__code__icontains=search_field)
            )
        filter_by_tag = self.request.GET.get("f")
        if filter_by_tag:
            queryset = queryset.order_by('order').filter(
                Q(client__slug=filter_by_tag)
                # | Q(app_label__icontains=fapp)
                )
        sort_by = self.request.GET.get("sort")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mdl = self.mdl
        context["columnames"] = table_balance
        context["sort_fields"] = self.sort_fields
        # context["nomenclature_type"] = nomenclature_type
        context["elems"] = buttons
        context["err_msg"] = msg["no_data_in_db"]
        context["add_url"] = reverse_lazy(mdl +"_create")
        context["this_url"] = reverse_lazy(mdl +"_list")
        context["title"] = mdlnames.get(mdl)
        search_field = self.request.GET.get("s")
        if search_field:
            context["s"] = f"s={search_field}&"
            context["title"] = mdlnames.get(mdl) + msg.get('search_title') + str(search_field)
        filter_by_client = self.request.GET.get("f")
        if filter_by_client:
            context["s"] = f"s={search_field}&"
            context["title"] = mdlnames.get(mdl) + msg.get('filter_title') + str(filter_by_client)
        sort_by = self.request.GET.get("sort")
        if sort_by:
            context["s"] = f"sort={sort_by}&"
        return context