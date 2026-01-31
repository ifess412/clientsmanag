from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from django.db.models import F
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.core.exceptions import PermissionDenied
# from django.contrib.auth.decorators import login_required
from django.apps import apps

from .models import *
from .forms import *

from logs.views import get_last_log

# from clients.libs.tableheads import *
# from clients.libs.adddata import *
# from clients.libs.settings import *

# Додаткові дані та налаштування
from libs.all_adddata import *
from libs.clients_adddata import *
from libs.settings import *
from libs.add_func import *

# for logging
# from .signals import *
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .middleware import get_current_request


APPL = "clients"

def index(request):
    return render(request, "clients/index.html")

def page_not_found_view(request, exception):
    return render(request, 'clients/404.html', status=404)

def redirect_to_external_site(request):
    external_url = "http://127.0.0.1:8000/admin/"  # Замініть на потрібний URL
    return redirect(external_url)

def clients_export_to_excel(request, model, orderby, filterrows):
    # print(model)
    MyModel = apps.get_model(APPL, model)
    response = export_to_excel(request, MyModel, orderby, filterrows)
    return response

def my_queryset(instance):
    # print(instance)
    thismodel = instance.model
    queryset = thismodel.objects.all()
    filter_by_client = instance.request.GET.get("f")
    if filter_by_client:
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

# def custom_permission_denied_view(request, exception=None):
#     return render(request, "clients/403.html", {}, status=403)

# @login_required
# def get_tag(request):
#     return render(request, "clients/main.html")

class MyListView(PermissionRequiredMixin, ListView):
    # id, name, app, idinapp, passinapp, comment, client, order, slug
    model = Access
    mdl = model._meta.model_name
    # mdl_name = model._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    # mdls = "tags"
    # mdl = "tag"
    context_object_name = "items"
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables
    # login_url = reverse_lazy('login')
    permission_required = APPL + ".view_" + mdl
    columnames = table_tags
    show_colums = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    sort_fields = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    # search_in_fields = ['name__icontains', 'name__icontains']
    add_data = {
        # 'addresstypes': addresstypes,
        # 'settltypes': settltypes,
    }


    def get_queryset(self):
        # thismodel = self.model
        # queryset = thismodel.objects.all()
        queryset = my_queryset(self)
        # filter_by_client = self.request.GET.get("f")
        # if filter_by_client:
        #     cfe = checkFieldExist(thismodel, 'order')
        #     if cfe:
        #         orderby = 'order'
        #     else:
        #         orderby = 'pk'
        #     queryset = queryset.order_by(orderby).filter(
        #         Q(client__slug=filter_by_client)
        #         # | Q(app_label__icontains=fapp)
        #         )
        # sort_by = self.request.GET.get("sort")
        # if sort_by:
        #     queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
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
        context["exp_url"] = reverse_lazy('export_to_excel')
        # context["title"] = mdlnames.get(mdls)
        context["title"] = mdl_name_pl
        context["mdl"] = mdl
        context["sort"] = 'pk'
        context["filter"] = ''
        search_field = self.request.GET.get("s")
        if search_field:
            context["s"] = f"s={search_field}&"
            context["title"] = mdl_name_pl + msg.get('search_title') + str(search_field)
            context["filter"] = search_field
        filter_by_client = self.request.GET.get("f")
        if filter_by_client:
            context["s"] = f"s={search_field}&"
            context["title"] = mdl_name_pl + msg.get('filter_title') + str(filter_by_client)
            context["filter"] = filter_by_client
        sort_by = self.request.GET.get("sort")
        if sort_by:
            context["sort"] = sort_by
            context["s"] = f"sort={sort_by}&"
        add_data = self.add_data
        if (add_data):
            for key, value in add_data.items():
                context[key] = value
        return context
    
class MyDetailView(PermissionRequiredMixin, DetailView):
    # model = Access
    model = Access
    mdl = model._meta.model_name
    # mdl_name = thismodel._meta.verbose_name
    # mdl_name_pl = model._meta.verbose_name_plural
    context_object_name = "item"
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_tags
    add_data = {
        # 'addresstypes': addresstypes,
        # 'settltypes': settltypes,
    }
        # add_data = self.add_data
        # if (add_data):
        #     for key, value in add_data.items():
        #         context[key] = value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thismodel = self.model
        mdl = thismodel._meta.model_name
        mdl_name = thismodel._meta.verbose_name
        mdl_name_pl = thismodel._meta.verbose_name_plural
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
        add_data = self.add_data
        if (add_data):
            for key, value in add_data.items():
                context[key] = value
        return context

class MyCreateView(PermissionRequiredMixin, CreateView):
    # form_class = TagForm
    model = Access
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
    model = Access
    mdl = model._meta.model_name
    # fields = ["title", "color"]
    context_object_name = "item"
    template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_tags

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
    model = Access
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

# class ClientListView(PermissionRequiredMixin, ListView):
#     model = Client
#     mdls = "clients"
#     context_object_name = "items"
#     template_name = "clients/" + mdls + "_list.html"
#     paginate_by = paginate_in_tables
#     login_url = reverse_lazy('login')
#     permission_required = "clients.view_client"
#     # redirect_field_name = 'clients'
#     # raise_exception = True

#     def get_queryset(self):
#         search_field = self.request.GET.get("s")
#         # table = self.request.GET.get("t")
#         if search_field:
#             search_field2 = search_field.capitalize()
#             searched = Client.objects.filter(
#                 Q(name__icontains=search_field)
#                 | Q(name__icontains=search_field2)
#                 | Q(fullname__icontains=search_field)
#                 | Q(code__icontains=search_field)
#             )
#         else: searched = Client.objects.all()
#         return searched

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdls = "clients"
#         context["columnames"] = table_clients
#         context["client_type"] = client_type
#         context["elems"] = buttons
#         context["title"] = mdlnames.get(mdls)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get("clients") + msg.get('search_title') + str(search_field)
#             context["err_msg"] = msg["no_data_in_db"]
#         return context

# class ClientDetailView(PermissionRequiredMixin, DetailView):
#     model = Client
#     mdls = "clients"
#     context_object_name = "item"
#     template_name = "clients/" + mdls + "_detail.html"
#     # permission_required = ("clients.view_client", "clients.add_client", "clients.change_client", "clients.delete_client")
#     permission_required = "clients.view_client"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["client_type"] = client_type
#         context["card_titles"] = card_clients
#         context["table_contacts"] = table_contacts
#         context["table_accesses"] = table_accesses
#         context["elems"] = buttons
#         mdls = "client"
#         obj_obj = Client.objects.get(slug=self.kwargs["slug"])
#         obj_str = str(obj_obj)
#         obj_id = obj_obj.id
#         context["title"] = (mdlnames.get(mdls) + ": " + obj_str)
#         lastupd = get_last_log(app_label=APPL, obj_model=mdls, obj_id=obj_id)
#         if (lastupd) :
#             context["lastupd"] = lastupd.date_time
#             context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
#         return context

# class ClientCreateView(PermissionRequiredMixin, CreateView):
#     form_class = ClientForm
#     # model = Client
#     mdls = "clients"
#     context_object_name = "item"
#     template_name = "clients/" + mdls + "_add.html"
#     success_url = reverse_lazy("client_list")
#     # permission_required = ("clients.view_client", "clients.add_client", "clients.change_client", "clients.delete_client")
#     permission_required = "clients.add_client"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["card_titles"] = card_clients
#         context["elems"] = buttons
#         mdls = "client"
#         context["title"] = msg.get("add") + mdlnames.get(mdls)
#         return context

# class ClientUpdateView(PermissionRequiredMixin, UpdateView):
#     form_class = ClientForm
#     model = Client
#     # fields = [
#     #     "name",
#     #     "code",
#     #     "fullname",
#     #     "address",
#     #     "comment",
#     #     "type",
#     #     "tags",
#     #     # "slug",
#     # ]
#     mdls = "clients"
#     context_object_name = "item"
#     template_name = "clients/" + mdls + "_add.html"
#     success_url = reverse_lazy("client_list")
#     permission_required = ("clients.view_client", "clients.change_client")
#     # login_url = reverse_lazy('login')
#     # raise_exception = False
#     # permission_denied_message = "!!!!!!!!!!!!!"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["card_titles"] = card_clients
#         context["elems"] = buttons
#         mdls = "client"
#         context["title"] = msg.get("edit") + mdlnames.get(mdls)
#         return context

# class ClientDeleteView(PermissionRequiredMixin, DeleteView):
#     # form_class = ClientForm
#     model = Client
#     fields = [
#         "name",
#     ]
#     template_name = "clients/single_delete.html"
#     success_url = reverse_lazy("client_list")
#     # permission_required = ("clients.view_client", "clients.add_client", "clients.change_client", "clients.delete_client")
#     permission_required =  "clients.delete_client"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["elems"] = buttons
#         context["msg"] = msg["del_question"]
#         context["title"] = msg.get("del_title")
#         context["back_url"] = reverse_lazy("client_list")
#         return context

class ClientListView(MyListView):
    # id, name, fullname, code, address, comment, type, tags, slug
    model = Client
    mdl = model._meta.model_name
    # mdls = "clients"
    # mdl = "client"
    template_name = APPL + "/" + mdl + "_list.html"
    # paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_clients
    show_colums = ['id', 'name','fullname', 'code','address', 'type', 'tags', 'pk']
    sort_fields = ['id', 'name', 'fullname','code', 'address','type', 'tags']
    # client_type = client_type
    add_data = {
        'client_type': client_type,
        # 'addresstypes': addresstypes,
        'settltypes': settltypes,
        'streettypes': streettypes,
        'apartmenttypes': apartmenttypes,
        # 'countries': countries,
        # 'regions': regions,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            # search_field2 = search_field.capitalize()
            # queryset = queryset.filter(
            #     Q(name__icontains=search_field) 
            #     # | Q(name__icontains=search_field2)
            #     | Q(name__iregex=search_field)
            #     | Q(fullname__icontains=search_field)
            #     | Q(code__icontains=search_field)
            #     )
            sf = search_field.split()
            search_firstword = sf[0]
            if search_firstword:
                queryset = queryset.filter(
                    Q(name__icontains=search_field) 
                    | Q(name__iregex=search_field)
                    | Q(fullname__icontains=search_field)
                    | Q(code__icontains=search_field)
                    | Q(fulladdresses__streetname__name__icontains=search_firstword) 
                    | Q(fulladdresses__streetname__name__iregex=search_firstword)
                    # | Q(oldstreetname__name__icontains=search_street)
                    # | Q(oldstreetname__name__iregex=search_street)
                    )
            if len(sf) > 1:
                search_housenum = sf[1]
                if search_housenum:
                    queryset = queryset.filter(
                        Q(fulladdresses__housenum__icontains=search_housenum) 
                        # | Q(streetname__name__iregex=search_field)
                        )
            if len(sf) > 2:
                search_apartment = sf[2]
                if search_apartment:
                    queryset = queryset.filter(
                        Q(fulladdresses__apartment__icontains=search_apartment) 
                        # | Q(streetname__name__iregex=search_field)
                        )
        return queryset
  

class ClientDetailView(MyDetailView):
    model = Client
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_clients
    # client_type = client_type
    # table_contacts = table_contacts
    # table_accesses = table_accesses
    # table_fulladdress = table_fulladdress
    add_data = {
        'client_type': client_type,
        'table_contacts': table_contacts,
        'table_accesses': table_accesses,
        'table_fulladdress': table_fulladdress,
        'addresstypes': addresstypes,
        'settltypes': settltypes,
        'streettypes': streettypes,
        'apartmenttypes': apartmenttypes,
    }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["client_type"] = self.client_type
    #     context["table_contacts"] = self.table_contacts
    #     context["table_accesses"] = self.table_accesses
    #     context["table_fulladdress"] = self.table_fulladdress
    #     # context["addresstypes"] = addresstypes
    #     # context["settltypes"] = settltypes
    #     context["streettypes"] = streettypes
    #     context["apartmenttypes"] = apartmenttypes
    #     return context

class ClientCreateView(MyCreateView):
    form_class = ClientForm
    model = Client
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class ClientUpdateView(MyUpdateView):
    form_class = ClientForm
    model = Client
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_clients

class ClientDeleteView(MyDeleteView):
    model = Client
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class ContactListView(MyListView):
    # id, name, phone1, phone2, phone3, email, comment, client, position, order, slug
    model = Contact
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_contacts
    show_colums = ['id', 'name','phone1', 'email','client', 'position', 'order', 'pk']
    sort_fields = ['id', 'name', 'email','client', 'position']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field) 
                | Q(name__icontains=search_field2)
                | Q(phone1__icontains=search_field)
                | Q(phone2__icontains=search_field)
                | Q(phone3__icontains=search_field)
                | Q(email__icontains=search_field)
                | Q(client__name=search_field)
                | Q(client__name=search_field2)
                )
        return queryset

class ContactDetailView(MyDetailView):
    model = Contact
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_contacts

class ContactCreateView(MyCreateView):
    form_class = ContactForm
    model = Contact
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class ContactUpdateView(MyUpdateView):
    form_class = ContactForm
    model = Contact
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_contacts

class ContactDeleteView(MyDeleteView):
    model = Contact
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

# class ContactListView(PermissionRequiredMixin, ListView):
#     model = Contact
#     mdls = "contacts"
#     context_object_name = "items"
#     template_name = "clients/" + mdls + "_list.html"
#     paginate_by = paginate_in_tables
#     login_url = reverse_lazy('login')
#     permission_required = "clients.view_contact"
#     # redirect_field_name = 'contact_list'
#     # raise_exception = True

#     def get_queryset(self):
#         queryset = Contact.objects.all()
#         search_field = self.request.GET.get("s")
#         if search_field:
#             search_field2 = search_field.capitalize()
#             queryset = queryset.filter(Q(name__icontains=search_field) | Q(name__icontains=search_field2))
#         filter_by_client = self.request.GET.get("f")
#         if filter_by_client:
#             queryset = queryset.order_by('order').filter(
#                 Q(client__slug=filter_by_client)
#                 # | Q(app_label__icontains=fapp)
#                 )
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdls = "contacts"
#         context["columnames"] = table_contacts
#         context["elems"] = buttons
#         context["title"] = mdlnames.get(mdls)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdls) + msg.get('search_title') + str(search_field)
#             context["err_msg"] = msg["no_data_in_db"]
#         filter_by_client = self.request.GET.get("f")
#         if filter_by_client:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdls) + msg.get('filter_title') + str(filter_by_client)
#             context["err_msg"] = msg["no_data_in_db"]
#         return context

# class ContactDetailView(PermissionRequiredMixin, DetailView):
#     model = Contact
#     mdls = "contacts"
#     context_object_name = "item"
#     template_name = "clients/" + mdls + "_detail.html"
#     permission_required = "clients.view_contact"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["card_titles"] = table_contacts
#         context["elems"] = buttons
#         mdls = "contact"
#         obj_obj = Contact.objects.get(slug=self.kwargs["slug"])
#         obj_str = str(obj_obj)
#         obj_id = obj_obj.id
#         context["title"] = (mdlnames.get(mdls) + ": " + obj_str)
#         lastupd = get_last_log(app_label=APPL, obj_model=mdls, obj_id=obj_id)
#         if (lastupd) :
#             context["lastupd"] = lastupd.date_time
#             context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
#         return context

# class ContactCreateView(PermissionRequiredMixin, CreateView):
#     form_class = ContactForm
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
#     mdls = "contacts"
#     context_object_name = "item"
#     template_name = "clients/" + mdls + "_add.html"
#     success_url = reverse_lazy("contact_list")
#     permission_required = "clients.add_contact"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["card_titles"] = table_contacts
#         context["elems"] = buttons
#         mdls = "contact"
#         context["title"] = msg.get("add") + mdlnames.get(mdls)
#         return context

# class ContactUpdateView(PermissionRequiredMixin, UpdateView):
#     form_class = ContactForm
#     model = Contact
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
#     mdls = "contacts"
#     context_object_name = "item"
#     template_name = "clients/" + mdls + "_add.html"
#     success_url = reverse_lazy("contact_list")
#     permission_required = "clients.change_contact"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["card_titles"] = table_contacts
#         context["elems"] = buttons
#         mdls = "contact"
#         context["title"] = msg.get("edit") + mdlnames.get(mdls)
#         return context

# class ContactDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Contact
#     fields = [
#         "name",
#     ]
#     template_name = "clients/single_delete.html"
#     success_url = reverse_lazy("contact_list")
#     permission_required = "clients.delete_contact"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["elems"] = buttons
#         context["msg"] = msg["del_question"]
#         context["title"] = msg.get("del_title")
#         context["back_url"] = reverse_lazy("contact_list")
#         return context

class AccessListView(MyListView):
    # id, name, app, idinapp, passinapp, comment, client, order, slug
    model = Access
    mdl = model._meta.model_name
    # context_object_name = "items"
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables
    # login_url = reverse_lazy('login')
    permission_required = APPL + ".view_" + mdl
    columnames = table_accesses
    show_colums = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client', 'order', 'pk']
    sort_fields = ['id', 'name', 'app', 'idinapp', 'passinapp', 'client']
    # search_in_fields = ['name__icontains', 'name__icontains', 'idinapp__icontains', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
                search_field2 = search_field.capitalize()
                queryset = queryset.filter(
                    Q(name__icontains=search_field)
                    | Q(name__icontains=search_field2)
                    # | Q(fullname__icontains=search_field)
                    # | Q(code__icontains=search_field)
                )
        return queryset
    
class AccessDetailView(MyDetailView):
    model = Access
    mdl = model._meta.model_name
    # context_object_name = "item"
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_accesses

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     mdl = self.mdl
    #     context["card_titles"] = table_accesses
    #     context["elems"] = buttons
    #     obj_obj = Access.objects.get(slug=self.kwargs["slug"])
    #     obj_str = str(obj_obj)
    #     obj_id = obj_obj.id
    #     context["title"] = (mdlnames.get(mdl) + ": " + obj_str)
    #     context["back_url"] = reverse_lazy(mdl +"_list")
    #     lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
    #     if (lastupd) :
    #         context["lastupd"] = lastupd.date_time
    #         context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
    #     return context

class AccessCreateView(MyCreateView):
    form_class = AccessForm
    model = Access
    mdl = model._meta.model_name
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class AccessUpdateView(MyUpdateView):
    form_class = AccessForm
    model = Access
    mdl = model._meta.model_name
    # context_object_name = "item"
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_accesses

class AccessDeleteView(MyDeleteView):
    model = Access
    mdl = model._meta.model_name
    # fields = [
    #     "name",
    # ]
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class TagListView(MyListView):
    # id, title, color, slug
    model = Tag
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_tags
    sort_fields = ['id', 'title', 'color']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(title__icontains=search_field)
                | Q(title__icontains=search_field2)
                # | Q(fullname__icontains=search_field)
                # | Q(code__icontains=search_field)
            )
        return queryset

class TagDetailView(MyDetailView):
    model = Tag
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_tags

class TagCreateView(MyCreateView):
    form_class = TagForm
    model = Tag
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class TagUpdateView(MyUpdateView):
    form_class = TagForm
    model = Tag
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_tags

class TagDeleteView(MyDeleteView):
    model = Tag
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

# class TagListView(PermissionRequiredMixin, ListView):
#     # id, title, color, slug
#     model = Tag
#     mdls = "tags"
#     mdl = "tag"
#     context_object_name = "items"
#     template_name = APPL + "/" + mdl + "_list.html"
#     paginate_by = paginate_in_tables
#     # login_url = reverse_lazy('login')
#     permission_required = APPL + ".view_" + mdl
#     sort_fields = ['id', 'title', 'color']

#     def get_queryset(self):
#         queryset = Tag.objects.all()
#         search_field = self.request.GET.get("s")
#         if search_field:
#             search_field2 = search_field.capitalize()
#             queryset = queryset.filter(
#                 Q(title__icontains=search_field)
#                 | Q(title__icontains=search_field2)
#                 # | Q(fullname__icontains=search_field)
#                 # | Q(code__icontains=search_field)
#             )
#         # filter_by_tag = self.request.GET.get("f")
#         # if filter_by_tag:
#         #     queryset = queryset.order_by('order').filter(
#         #         Q(client__slug=filter_by_tag)
#         #         # | Q(app_label__icontains=fapp)
#         #         )
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             queryset = queryset.order_by(sort_by)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdls = self.mdls
#         mdl = self.mdl
#         context["sort_fields"] = self.sort_fields
#         context["columnames"] = table_tags
#         context["elems"] = buttons
#         context["err_msg"] = msg["no_data_in_db"]
#         context["new_url"] = reverse_lazy(mdl +"_create")
#         context["this_url"] = reverse_lazy(mdl +"_list")
#         context["add_url"] = mdl +"_add"
#         context["dtl_url"] = mdl +"_detail"
#         context["upd_url"] = mdl +"_update"
#         context["del_url"] = mdl +"_delete"
#         context["title"] = mdlnames.get(mdls)
#         search_field = self.request.GET.get("s")
#         if search_field:
#             context["s"] = f"s={search_field}&"
#             context["title"] = mdlnames.get(mdl) + msg.get('search_title') + str(search_field)
#         # filter_by_client = self.request.GET.get("f")
#         # if filter_by_client:
#         #     context["s"] = f"s={search_field}&"
#         #     context["title"] = mdlnames.get(mdl) + msg.get('filter_title') + str(filter_by_client)
#         sort_by = self.request.GET.get("sort")
#         if sort_by:
#             context["s"] = f"sort={sort_by}&"
#         return context
    
# class TagDetailView(PermissionRequiredMixin, DetailView):
#     model = Tag
#     mdl = "tag"
#     context_object_name = "item"
#     template_name = APPL + "/" + mdl + "_detail.html"
#     permission_required = APPL + ".view_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["card_titles"] = table_tags
#         context["elems"] = buttons
#         obj_obj = Tag.objects.get(slug=self.kwargs["slug"])
#         obj_str = str(obj_obj)
#         obj_id = obj_obj.id
#         context["title"] = (mdlnames.get(mdl) + ": " + obj_str)
#         context["back_url"] = reverse_lazy(mdl +"_list")
#         lastupd = get_last_log(app_label=APPL, obj_model=mdl, obj_id=obj_id)
#         if (lastupd) :
#             context["lastupd"] = lastupd.date_time
#             context["lastupdby"] = lastupd.user.first_name if lastupd.user.first_name else lastupd.user.username
#         return context

# class TagCreateView(PermissionRequiredMixin, CreateView):
#     form_class = TagForm
#     # model = Tag
#     # fields = ["title", "color"]
#     mdl = "tag"
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl +"_list")
#     permission_required = APPL + ".add_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["elems"] = buttons
#         context["title"] = msg.get("add") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl +"_list")
#         return context

# class TagUpdateView(PermissionRequiredMixin, UpdateView):
#     form_class = TagForm
#     model = Tag
#     mdl = "tag"
#     # fields = ["title", "color"]
#     context_object_name = "item"
#     template_name = APPL + "/single_add.html"
#     success_url = reverse_lazy(mdl + "_list")
#     permission_required = APPL + ".change_" + mdl

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mdl = self.mdl
#         context["card_titles"] = table_tags
#         context["elems"] = buttons
#         context["title"] = msg.get("edit") + mdlnames.get(mdl)
#         context["back_url"] = reverse_lazy(mdl + "_list")
#         return context

# class TagDeleteView(PermissionRequiredMixin, DeleteView):
#     model = Tag
#     fields = [
#         "title",
#     ]
#     template_name = "clients/single_delete.html"
#     success_url = reverse_lazy("tag_list")
#     permission_required = "clients.delete_tag"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["elems"] = buttons
#         context["msg"] = msg["del_question"]
#         context["title"] = msg.get("del_title")
#         context["back_url"] = reverse_lazy("tag_list")
#         return context

# FilterByTag
class FilterByTag(PermissionRequiredMixin, ListView):
    template_name = "clients/clients_list.html"
    context_object_name = "items"
    paginate_by = paginate_in_tables
    # allow_empty = False
    permission_required = "clients.view_client"

    def get_queryset(self):
        return Client.objects.filter(tags__slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["columnames"] = table_clients
        context["client_type"] = client_type
        context["err_msg"] = msg["no_data_in_db"]
        context["elems"] = buttons
        context["title"] = msg.get("filter_by_tag") + str(
            Tag.objects.get(slug=self.kwargs["slug"])
        )
        return context

# class Search(ListView):
#     template_name = "clients/clients_list.html"
#     context_object_name = "items"
#     paginate_by = paginate_in_tables

#     def get_template_names(self):
#         table = self.request.GET.get("t")
#         if table == "clients":
#             self.template_name = "clients/clients_list.html"
#         elif table == "contacts":
#             self.template_name = "clients/contacts_list.html"
#         elif table == "access":
#             self.template_name = "clients/access_list.html"
#         return [self.template_name]

#     def get_queryset(self):
#         search_field = self.request.GET.get("s")
#         search_field2 = search_field.capitalize()
#         table = self.request.GET.get("t")
#         if table == "clients":
#             searched = Client.objects.filter(
#                 Q(name__icontains=search_field)
#                 | Q(name__icontains=search_field2)
#                 | Q(fullname__icontains=search_field)
#                 | Q(code__icontains=search_field)
#             )
#         elif table == "contacts":
#             searched = Contact.objects.filter(Q(name__icontains=search_field) | Q(name__icontains=search_field2))
#         elif table == "access":
#             searched = Access.objects.filter(Q(name__icontains=search_field) | Q(name__icontains=search_field2))
#         # return Client.objects.filter(name__icontains=self.request.GET.get("s"))
#         return searched

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         search_field = self.request.GET.get("s")
#         table = self.request.GET.get("t")
#         if table == "clients":
#             context["columnames"] = table_clients
#             context["client_type"] = client_type
#             context["title"] = mdlnames.get("clients") + msg.get('search_title') + str(search_field)
#         elif table == "contacts":
#             context["columnames"] = table_contacts
#             context["title"] = mdlnames.get("contacts") + msg.get('search_title') + str(search_field)
#         elif table == "access":
#             context["columnames"] = table_accesses
#             context["title"] = mdlnames.get("accesses") + msg.get('search_title') + str(search_field)
#         context["s"] = f"s={search_field}&"
#         context["err_msg"] = msg["no_data_in_db"]
#         context["elems"] = buttons
#         # context["title"] = "Пошук: " + str(search_field)
#         return context
    
# Address 
class CityListView(MyListView):
    # id, name, slug
    model = City
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_cities
    show_colums = ['id', 'name', 'pk']
    sort_fields = ['id', 'name']
    add_data = {
        'settltypes': settltypes,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field) 
                | Q(name__icontains=search_field2)
                | Q(name__iregex=search_field)
                )
        return queryset
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["settltypes"] = settltypes
    #     return context

class CityDetailView(MyDetailView):
    model = City
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_cities
    add_data = {
        'settltypes': settltypes,
    }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["settltypes"] = settltypes
    #     return context

class CityCreateView(MyCreateView):
    form_class = CityForm
    model = City
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class CityUpdateView(MyUpdateView):
    form_class = CityForm
    model = City
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_cities

class CityDeleteView(MyDeleteView):
    model = City
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class DistrListView(MyListView):
    # id, name, slug
    model = Distr
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    # paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_citydistr
    show_colums = ['id', 'name', 'pk']
    sort_fields = ['id', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field) 
                | Q(name__icontains=search_field2)
                )
        return queryset

class DistrDetailView(MyDetailView):
    model = Distr
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_citydistr

class DistrCreateView(MyCreateView):
    form_class = DistrForm
    model = Distr
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class DistrUpdateView(MyUpdateView):
    form_class = DistrForm
    model = Distr
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_citydistr

class DistrDeleteView(MyDeleteView):
    model = Distr
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class StreetListView(MyListView):
    # id, name, slug
    model = Street
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    # paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_street
    show_colums = ['id', 'name','distr','archive','pk']
    sort_fields = ['id', 'name','distr']
    add_data = {
        'streettypes': streettypes,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            search_field2 = search_field.capitalize()
            queryset = queryset.filter(
                Q(name__icontains=search_field) 
                | Q(name__icontains=search_field2)
                | Q(name__iregex=search_field)
                )
        return queryset

class StreetDetailView(MyDetailView):
    model = Street
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_street
    add_data = {
        'streettypes': streettypes,
    }

class StreetCreateView(MyCreateView):
    form_class = StreetForm
    model = Street
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class StreetUpdateView(MyUpdateView):
    form_class = StreetForm
    model = Street
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_citydistr

class StreetDeleteView(MyDeleteView):
    model = Street
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl

class FulladdressListView(MyListView):
    # client, addresstype, index, country, region, settltype, cityname, ​distr, 
    # streettype, streetname, oldstreetname, housenum, apartmenttype, apartment, entrance, floor, comment
    model = Fulladdress
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_list.html"
    # paginate_by = paginate_in_tables
    permission_required = APPL + ".view_" + mdl
    columnames = table_fulladdress
    show_colums = ['id', 'client', 'addresstype', 'cityname',  'streetname', 'oldstreetname', 'housenum', 'apartment', 'pk']
    sort_fields = ['id', 'client', 'addresstype', 'country', 'region', 'cityname', 'distr',  'streetname', 'oldstreetname', 'housenum', 'apartment']
    add_data = {
        'addresstypes': addresstypes,
        'settltypes': settltypes,
        'streettypes': streettypes,
        'apartmenttypes': apartmenttypes,
        'countries': countries,
        'regions': regions,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_field = self.request.GET.get("s")
        if search_field:
            sf = search_field.split()
            search_street = sf[0]
            if search_street:
                queryset = queryset.filter(
                    Q(streetname__name__icontains=search_street) 
                    | Q(streetname__name__iregex=search_street)
                    | Q(oldstreetname__name__icontains=search_street)
                    | Q(oldstreetname__name__iregex=search_street)
                    )
            if len(sf) > 1:
                search_housenum = sf[1]
                if search_housenum:
                    queryset = queryset.filter(
                        Q(housenum__icontains=search_housenum) 
                        # | Q(streetname__name__iregex=search_field)
                        )
            if len(sf) > 2:
                search_apartment = sf[2]
                if search_apartment:
                    queryset = queryset.filter(
                        Q(apartment__icontains=search_apartment) 
                        # | Q(streetname__name__iregex=search_field)
                        )
            # search_field2 = search_field.capitalize()
            # queryset = queryset.filter(
            #     Q(streetname__name__icontains=search_field) 
            #     | Q(streetname__name__iregex=search_field)
            #     )
        return queryset
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["addresstypes"] = addresstypes
    #     context["settltypes"] = settltypes
    #     context["streettypes"] = streettypes
    #     context["apartmenttypes"] = apartmenttypes
    #     context["countries"] = countries
    #     context["regions"] = regions
    #     return context

class FulladdressDetailView(MyDetailView):
    model = Fulladdress
    mdl = model._meta.model_name
    template_name = APPL + "/" + mdl + "_detail.html"
    permission_required = APPL + ".view_" + mdl
    card_titles = table_fulladdress
    add_data = {
        'addresstypes': addresstypes,
        'settltypes': settltypes,
        'streettypes': streettypes,
        'apartmenttypes': apartmenttypes,
        'countries': countries,
        'regions': regions,
    }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["addresstypes"] = addresstypes
    #     context["settltypes"] = settltypes
    #     context["streettypes"] = streettypes
    #     context["apartmenttypes"] = apartmenttypes
    #     context["countries"] = countries
    #     context["regions"] = regions
    #     return context

class FulladdressCreateView(MyCreateView):
    form_class = FulladdressForm
    model = Fulladdress
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl +"_list")
    permission_required = APPL + ".add_" + mdl

class FulladdressUpdateView(MyUpdateView):
    form_class = FulladdressForm
    model = Fulladdress
    mdl = model._meta.model_name
    # template_name = APPL + "/single_add.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".change_" + mdl
    card_titles = table_fulladdress

class FulladdressDeleteView(MyDeleteView):
    model = Fulladdress
    mdl = model._meta.model_name
    # template_name = APPL + "/single_delete.html"
    success_url = reverse_lazy(mdl + "_list")
    permission_required = APPL + ".delete_" + mdl


