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
from django.http import JsonResponse
# from django.utils.timezone import now
# import datetime
from datetime import date, timedelta
# from dateutil.relativedelta import relativedelta
from django.db.models import Max
from django.apps import apps

from .models import *
from .forms import *
# from .forms import NomenclatureForm, PriceForm, DiscountForm, CashbookForm, BalanceForm,

# # Додаткові дані та налаштування
# from libs.all_adddata import *
# from libs.finances_adddata import *
# from libs.settings import *
# from libs.add_func import *

# Додаткові дані та налаштування
from libs.addata_all import *
from libs.addata_finances import *
from libs.confs import *
from libs.add_func import *

# # for logging
# from .signals import *
# signals imported in app
from logs.views import get_last_log

APPL = "finances"

# Сегодня без времени
today = date.today()
# Минус 1 месяц
some_days_ago = today - timedelta(days=days_ago)
some_days_later = today + timedelta(days=days_later)

# def get_columnames(formodel):
#     columnames = {
#         # 'username': request.user.username,
#     }
#     for f in formodel._meta.fields:
#         columnames[f.name] = f.verbose_name
#     # columnames = [f.verbose_name for f in model._meta.fields]
#     columnames['pk'] = 'Дії'
#     # columnames.append('Дії')
#     # print(type(columnames))
#     # print(columnames)
#     return columnames


def get_next_doc_number(request):
    # Отримуємо назву моделі з GET-параметра (наприклад, 'license')
    model_name = request.GET.get('model')
    
    if not model_name:
        return JsonResponse({'error': 'Параметр model обовʼязковий'}, status=400)
    
    try:
        # Динамічно отримуємо клас моделі. 
        # Замініть 'finances' на назву вашого Django-додатку (app), де лежать моделі
        ModelClass = apps.get_model('finances', model_name)
        
        # Шукаємо максимальний номер у полі 'num' для цієї конкретної моделі
        max_num = ModelClass.objects.aggregate(Max('num'))['num__max']
        
        # Якщо записів немає, починаємо з 1
        next_number = (max_num or 0) + 1
        
        return JsonResponse({'next_number': next_number})
        
    except LookupError:
        # Якщо модель з такою назвою не знайдена в додатку
        return JsonResponse({'error': f'Модель {model_name} не знайдена'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_lic_price_json(request):
    getted_id = request.GET.get('id')
    model = Price
    # print(getted_id)
    try:
        model_obj = model.objects.get(nomenclature__pk=getted_id)
        # print(model_obj.price)
        return JsonResponse({'price': model_obj.price})
    except model.DoesNotExist:
        # return JsonResponse({'price': 0}, status=404)
        return JsonResponse({'price': 0})

def get_discount_json(request):
    getted_id = request.GET.get('id')
    model = Discount
    # print(getted_id)
    try:
        model_obj = model.objects.get(client__pk=getted_id)
        return JsonResponse({'price': model_obj.discount})
    except model.DoesNotExist:
        # return JsonResponse({'price': 0}, status=404)
        return JsonResponse({'price': 0})


def get_paydirection(instance):
    # payment direction
    initform = {}
    obj_obj = Client.objects.get(type=0)
    if obj_obj:
        my_org_id = obj_obj.id
        direction = instance.request.GET.get("direction")
        if direction == 'in':
            initform = {'payee': my_org_id}
        elif direction == 'out':
            initform = {'payer': my_org_id}
    return initform

def my_queryset(instance):
    # print(instance)
    thismodel = instance.model
    queryset = thismodel.objects.all()
    filter_by_client = instance.request.GET.get("f")
    if filter_by_client:
        cfe = checkFieldExist(thismodel, 'docdate')
        if cfe:
            orderby = '-docdate'
        else:
            cfe = checkFieldExist(thismodel, 'order')
            if cfe:
                orderby = 'order'
            else:
                orderby = 'pk'
        queryset = queryset.order_by(orderby).filter(
            Q(client__slug=filter_by_client)
            # | Q(app_label__icontains=fapp)
            )
    sort_by = instance.request.GET.get("sort")
    if sort_by:
        queryset = queryset.order_by(sort_by)
    return queryset

class MyListView(PermissionRequiredMixin, ListView):
    # 
    model = Cashbook
    mdl = model._meta.model_name
    # mdl_name = model._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    context_object_name = "items"
    template_name = APPL + "/" + mdl + "_list.html"
    # paginate_by = paginate_in_tables_finance
    permission_required = APPL + ".view_" + mdl
    # columnames = table_nomenclature
    columnames = get_columnames(model)
    show_colums = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    sort_fields = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    # search_in_fields = ['name__icontains', 'name__icontains']
    add_data = {
        # 'addresstypes': addresstypes,
    }

    def get_paginate_by(self, queryset):
        # Отримуємо 'page_size' з URL, наприклад ?page_size=10
        # За замовчуванням paginate_in_tables
        return self.request.GET.get('page_size', paginate_in_tables)

    # def get_queryset(self):
    #     thismodel = self.model
    #     queryset = thismodel.objects.all()
    #     filter_by_client = self.request.GET.get("f")
    #     if filter_by_client:
    #         queryset = queryset.order_by('order').filter(
    #             Q(client__slug=filter_by_client)
    #             # | Q(app_label__icontains=fapp)
    #             )
    #     sort_by = self.request.GET.get("sort")
    #     if sort_by:
    #         queryset = queryset.order_by(sort_by)
    #     return queryset
    
    def get_queryset(self):
        queryset = my_queryset(self)
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
        context["msg"] = msg
        context["err_msg"] = msg["no_data_in_db"]
        context["new_url"] = reverse_lazy(mdl +"_create")
        context["this_url"] = reverse_lazy(mdl +"_list")
        context["add_url"] = mdl +"_add"
        context["dtl_url"] = mdl +"_detail"
        context["upd_url"] = mdl +"_update"
        context["del_url"] = mdl +"_delete"
        context["exp_url"] = reverse_lazy('export_to_excel')
        context["back_url"] = self.request.META.get('HTTP_REFERER', 'home')
        # context["doc_url"] = reverse_lazy('export_to_excel')
        context["title"] = mdl_name_pl
        context["mdl"] = mdl
        context["sort"] = 'pk'
        context["filter"] = ''
        context["page_sizes"] = paginate_by_size
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
        page_size = self.request.GET.get("page_size")
        if page_size:
            context["page_size"] = page_size
            context["s"] = f"page_size={page_size}&"
        add_data = self.add_data
        if (add_data):
            for key, value in add_data.items():
                context[key] = value
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
    add_data = {
        # 'addresstypes': addresstypes,
    }

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
        # context["back_url"] = reverse_lazy(mdl +"_list")
        context["back_url"] = self.request.META.get('HTTP_REFERER', 'home')
        lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
        if (lastupd) :
            context["lastupd"] = lastupd.date_time
            context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
        add_data = self.add_data
        if (add_data):
            for key, value in add_data.items():
                context[key] = value
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
    # columnames = get_columnames(model)
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

def BalanceCreateItem(request):
    model = Balance
    mdl = model._meta.model_name
    search_field = request.GET.get("i")
    if search_field:
        C1 = Client.objects.get(name=search_field)
        new = Balance.objects.create(client=C1, balance=0)
        return redirect(mdl +"_update", pk=new.pk)
    else: return redirect(mdl +"_create")

class BalanceListView(MyListView):
    #  name, fullname, code
    model = Balance
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_balance
    show_colums = ['id', 'code', 'name', 'fullname', 'balance__balance', 'pk']
    sort_fields = ['id', 'code', 'name', 'fullname', 'balance__balance']

    def get_queryset(self):
        # name, fullname, code
        queryset = super().get_queryset()
        queryset = Client.objects.values('pk', 'code', 'name', 'fullname', 'slug', 'balance__pk', 'balance__balance')
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
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context["nomenclature_type"] = nomenclature_type
    #     return context

class BalanceDetailView(MyDetailView):
    model = Balance
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_balance

class BalanceCreateView(MyCreateView):
    form_class = BalanceForm
    model = Balance
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class BalanceUpdateView(MyUpdateView):
    form_class = BalanceForm
    model = Balance
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_balance

class BalanceDeleteView(MyDeleteView):
    model = Balance
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class CashbookListView(MyListView):
    # id, num, datedoc, payer, payee, sum, paytype, paystatus, comment
    model = Cashbook
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_cashbook
    show_colums = ['id', 'num','datedoc', 'payer','payee', 'sum', 'paytype', 'paystatus',  'pk']
    sort_fields = ['id', 'num','datedoc', 'payer','payee', 'sum', 'paytype', 'paystatus']
    add_data = {
        'paytypes': paytypes,
        'paystatuses': paystatuses,
    }

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_field = self.request.GET.get("s")
    #     if search_field:
    #         # search_field2 = search_field.capitalize()
    #         # queryset = queryset.filter(
    #         #     Q(name__icontains=search_field) 
    #         #     # | Q(name__icontains=search_field2)
    #         #     | Q(name__iregex=search_field)
    #         #     | Q(fullname__icontains=search_field)
    #         #     | Q(code__icontains=search_field)
    #         #     )
    #      return queryset

class CashbookDetailView(MyDetailView):
    model = Cashbook
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_cashbook
    add_data = {
        'paytypes': paytypes,
        'paystatuses': paystatuses,
    }

class CashbookCreateView(MyCreateView):
    form_class = CashbookForm
    model = Cashbook
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['payer'] = 59
    #     return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = get_paydirection(self)
        # kwargs['initial'] = {'payee': 59}
        # kwargs['initial'] = {'payee': self.request.user}
        return kwargs

class CashbookUpdateView(MyUpdateView):
    form_class = CashbookForm
    model = Cashbook
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    # card_titles = table_cashbook

class CashbookDeleteView(MyDeleteView):
    model = Cashbook
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class TransactionListView(MyListView):
    # id, client, sum, datetime, balance, docapp, docmodel, docid
    # 'id', 'client', 'sum', 'datetime', 'balance', 'docapp', 'docmodel', 'docid'
    model = Transaction
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_transaction
    # columnames = get_columnames(model)
    show_colums = ['id', 'client', 'sum', 'datedoc', 'docapp', 'docmodel', 'docid','datetime', 'pk']
    sort_fields = ['id', 'client', 'sum', 'datedoc', 'balance', 'docapp', 'docmodel', 'docid', 'datetime']
    # updbalance = balance_get_or_update(Balance, clientid, sum)
    add_data = {
        # 'objtitle': "Balance now: ",
        # 'paystatuses': paystatuses,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        fclient = self.request.GET.get("fclient")
        if fclient:
            queryset = queryset.filter(
                Q(client__name__icontains=fclient)
                | Q(client__name__iregex=fclient)
                )
        fapp = self.request.GET.get("fapp")
        if fapp:
            queryset = queryset.filter(
                Q(docapp__icontains=fapp)
                | Q(docapp__icontains=fapp)
                )
        fmodel = self.request.GET.get("fmodel")
        if fmodel:
            queryset = queryset.filter(
                Q(docmodel__icontains=fmodel)
                | Q(docmodel__icontains=fmodel)
                )
        fid = self.request.GET.get("fid")
        if fid:
            queryset = queryset.filter(docid=fid)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_by_client = self.request.GET.get("f")
        if filter_by_client:
            clientslug = filter_by_client
            obj_obj = getOneObj(Client, clientslug)
            balancenow = balance_get_or_update(Balance, obj_obj, sum=0)
            context["objtitle"] = "Balance now: " + str(balancenow)
        context["back_url"] = reverse_lazy('balance_list')
        return context

class TransactionDeleteView(MyDeleteView):
    model = Transaction
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class LicenseListView(MyListView):
    # id, num, client, nomenclature, price, orderdate, enddate, pccode, licensecode, seller, 
    # developer, devdiscount, devprice, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment
    model = License
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_license
    show_colums = ['id', 'num', 'client', 'nomenclature', 'price', 'orderdate', 'enddate', 'pk']
    sort_fields = ['id', 'num', 'client', 'nomenclature', 'price', 'orderdate', 'enddate', 'seller']
    add_data = {
        # 'now': now(),
        'now': today,
        'ago': some_days_ago,
        'later': some_days_later,
        # 'paystatuses': paystatuses,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
    #         # search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(client__name__icontains=search_field)
                | Q(client__code__icontains=search_field) 
                | Q(nomenclature__name__icontains=search_field) 
                | Q(client__name__iregex=search_field) 
    #         #     # | Q(name__icontains=search_field2)
    #         #     | Q(name__iregex=search_field)
    #         #     | Q(fullname__icontains=search_field)
    #         #     | Q(code__icontains=search_field)
            )
        filter_by_date = self.request.GET.get("fd")
        if filter_by_date:
            queryset = queryset.filter(
                Q(enddate__gt=filter_by_date)
                # | Q(enddate__gt=some_days_ago)
                # | Q(app_label__icontains=fapp)
                )
        return queryset

class LicenseDetailView(MyDetailView):
    model = License
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_license
    add_data = {
        # 'paytypes': paytypes,
        # 'paystatuses': paystatuses,
    }

class LicenseCreateView(MyCreateView):
    form_class = LicenseForm
    model = License
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['payer'] = 59
    #     return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = get_paydirection(self)
        # kwargs['initial'] = {'payee': 59}
        # kwargs['initial'] = {'payee': self.request.user}
        return kwargs

class LicenseUpdateView(MyUpdateView):
    form_class = LicenseForm
    model = License
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    # card_titles = table_cashbook

class LicenseDeleteView(MyDeleteView):
    model = License
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class ActListView(MyListView):
    # id, num, datedoc, client, nomenclature, price, seller, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment
    model = Act
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    permission_required = APPL + ".view_" + mdl
    columnames = table_act
    show_colums = ['id', 'num', 'datedoc', 'seller', 'client', 'nomenclature', 'price', 'agent', 'pk']
    sort_fields = ['id', 'num', 'datedoc', 'seller', 'client', 'nomenclature', 'price', 'agent' ]
    add_data = {
        # 'paytypes': paytypes,
        # 'paystatuses': paystatuses,
    }

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_field = self.request.GET.get("s")
    #     if search_field:
    # #         # search_field2 = search_field.capitalize()
    #         queryset = queryset.filter(
    #             Q(client__name__icontains=search_field)
    #             | Q(client__code__icontains=search_field) 
    #             | Q(nomenclature__name__icontains=search_field) 
    #             | Q(client__name__iregex=search_field) 
    # #         #     # | Q(name__icontains=search_field2)
    # #         #     | Q(name__iregex=search_field)
    # #         #     | Q(fullname__icontains=search_field)
    # #         #     | Q(code__icontains=search_field)
    #         )
    #     filter_by_date = self.request.GET.get("fd")
    #     if filter_by_date:
    #         queryset = queryset.filter(
    #             Q(enddate__gt=filter_by_date)
    #             # | Q(enddate__gt=some_days_ago)
    #             # | Q(app_label__icontains=fapp)
    #             )
    #     return queryset

class ActDetailView(MyDetailView):
    model = Act
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_act
    add_data = {
        # 'paytypes': paytypes,
        # 'paystatuses': paystatuses,
    }

class ActCreateView(MyCreateView):
    form_class = ActForm
    model = Act
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['payer'] = 59
    #     return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = get_paydirection(self)
        # kwargs['initial'] = {'payee': 59}
        # kwargs['initial'] = {'payee': self.request.user}
        return kwargs

class ActUpdateView(MyUpdateView):
    form_class = ActForm
    model = Act
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    # card_titles = table_cashbook

class ActDeleteView(MyDeleteView):
    model = Act
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

 
