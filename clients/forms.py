from django import forms
from django.core.validators import RegexValidator
from django_select2.forms import Select2Widget, ModelSelect2Widget

# import re
# from django.core.exceptions import ValidationError

from .models import Client, Contact, Access, Tag, City, Distr, Street, Fulladdress
from libs.clients_adddata import client_type
from libs.add_address import addresstypes, countries, regions, settltypes, streettypes, apartmenttypes

# from libs.add_address import addresstype
# from libs.all_adddata import msg


class ClientForm(forms.ModelForm):
    # id, name, fullname, code, address, comment, type, tags, slug
    class Meta:
        model = Client
        # fields = "__all__"
        fields = [
            "name",
            "code",
            "fullname",
            "address",
            "comment",
            "type",
            "tags",
            # "slug",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            # "code": forms.IntegerField(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # "type": forms.ChoiceField(
            #     choices=client_type, attrs={"class": "form-control"}
            # ),
            # "tags": forms.CheckboxSelectMultiple(attrs={"class": "form-control"}
            # ),
            # "category": forms.Select(attrs={"class": "form-control"}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data["title"]
    #     if re.match(r"\d", title):
    #         raise ValidationError("Название не должно начинаться с цифры")
    #     return title
        
class ContactForm(forms.ModelForm):
    # id, name, phone1, phone2, phone3, email, comment, client, position, order, slug

    phonevalidator = RegexValidator(
        regex=r"^\+?\d{1,4}?\s?\d{1,14}\s?\d{1,14}$",
        message="Вкажіть контактний телефон у форматі +380 XX XXX-XX-XX",
        code="invalid_phone_number",
    )

    class Meta:
        model = Contact
        # fields = "__all__"
        fields = [
            "name",
            "phone1",
            "phone2",
            "phone3",
            "email",
            "client",
            "position",
            "order",
            "comment",
            # "slug",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone1": forms.TextInput(attrs={"class": "form-control"}),
            "phone2": forms.TextInput(attrs={"class": "form-control"}),
            "phone3": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # "type": forms.ChoiceField(
            #     choices=client_type, attrs={"class": "form-control"}
            # ),
            # "tags": forms.TypedMultipleChoiceField(
            #     choices=client_type, attrs={"class": "form-control"}
            # ),
            # "category": forms.Select(attrs={"class": "form-control"}),
        }

class AccessForm(forms.ModelForm):
    # id, name, app, idinapp, passinapp, comment, client, order, slug

    class Meta:
        model = Access
        # fields = "__all__"
        fields = [
            "name",
            "app",
            "idinapp",
            "passinapp",
            "client",
            "order",
            "comment",
            # "slug",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # "app": forms.TextInput(attrs={"class": "form-control"}),
            "idinapp": forms.TextInput(attrs={"class": "form-control"}),
            "passinapp": forms.TextInput(attrs={"class": "form-control"}),
            # "email": forms.EmailInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # "type": forms.ChoiceField(
            #     choices=client_type, attrs={"class": "form-control"}
            # ),
            # "tags": forms.TypedMultipleChoiceField(
            #     choices=client_type, attrs={"class": "form-control"}
            # ),
            # "category": forms.Select(attrs={"class": "form-control"}),
        }

class TagForm(forms.ModelForm):
    # id, title, color, slug
    class Meta:
        model = Tag
        # fields = "__all__"
        fields = [
            "title",
            "color",
            # "code",
            # "address",
            # "comment",
            # "type",
            # "tag",
            # "slug",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            # "code": forms.TextInput(attrs={"class": "form-control"}),
            # "code": forms.IntegerField(required=False, attrs={"class": "form-control"}),
            # "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # "type": forms.ChoiceField(
            #     choices=client_type, attrs={"class": "form-control"}
            # ),
            # "tags": forms.CheckboxSelectMultiple(attrs={"class": "form-control"}
            # ),
            # "category": forms.Select(attrs={"class": "form-control"}),
        }

class CityForm(forms.ModelForm):
    # id, name, slug
    settltype = forms.ChoiceField(
        choices=settltypes,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=0,
        label='Тип населенного пункту'
    )
        
    class Meta:
        model = City
        # fields = "__all__"
        fields = [
            'settltype',
            "name",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # "color": forms.TextInput(attrs={"class": "form-control"}),
        }

class DistrForm(forms.ModelForm):
    # id, name, slug
    class Meta:
        model = Distr
        # fields = "__all__"
        fields = [
            "name",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # "color": forms.TextInput(attrs={"class": "form-control"}),
        }

class StreetForm(forms.ModelForm):
    # id, name, slug
    streettype = forms.ChoiceField(
        choices=streettypes,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=0,
        label='Тип вулиці'
    )

    class Meta:
        model = Street
        # fields = "__all__"
        fields = [
            "streettype",
            "name",
            # 'fullname',
            'distr',
            'archive',
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # "fullname": forms.TextInput(attrs={"class": "form-control"}),
            "arсhive": forms.CheckboxInput(attrs={"class": "form-control"}),
            # "name": forms.TextInput(attrs={"class": "form-control"}),
            # "color": forms.TextInput(attrs={"class": "form-control"}),
        }

class FulladdressForm(forms.ModelForm):
    # client, addresstype, index, country, region, settltype, cityname, distr, 
    # streettype, streetname, oldstreetname, housenum, apartmenttype, apartment, entrance, floor, comment
        
    # Відображається пошуковою строкою з спадаючим списком:
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Кліент",
        widget=ModelSelect2Widget(
            model=Client,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'fullname__icontains', 'code__icontains', 'name__iregex'], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    # Відображається спадаючим списком:
    addresstype = forms.ChoiceField(
        choices=addresstypes,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        label='Тип адреси'
    )
    country = forms.ChoiceField(
        choices=countries,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=1,
        label='Країна'
    )
    region = forms.ChoiceField(
        choices=regions,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        # initial=0,
        label='Область'
    )
    # settltype = forms.ChoiceField(
    #     choices=settltypes,
    #     widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
    #     initial=0,
    #     label='Тип населенного пункту'
    # )

    # Відображається спадаючим списком:
    cityname = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Місто")
    # Відображається пошуковою строкою з спадаючим списком:
    # cityname = forms.ModelChoiceField(
    #     queryset=City.objects.all(),
    #     label="Місто",
    #     widget=ModelSelect2Widget(
    #         model=City,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    # Відображається спадаючим списком:
    distr = forms.ModelChoiceField(
        queryset=Distr.objects.all(),
        required=False, 
        widget=forms.Select(attrs={"class": "form-control" }), 
        label="Район міста (оберіть тут, якщо район для цієї адреси відрізняється від району всієї вулиці)")
    # Відображається пошуковою строкою з спадаючим списком:
    # distr = forms.ModelChoiceField(
    #     queryset=Distr.objects.all(),
    #     label="Район міста",
    #     widget=ModelSelect2Widget(
    #         model=Distr,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    # streettype = forms.ChoiceField(
    #     choices=streettypes,
    #     widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
    #     initial=0,
    #     label='Тип вулиці'
    # )
    # Відображається пошуковою строкою з спадаючим списком:
    streetname = forms.ModelChoiceField(
        queryset=Street.objects.filter(archive=False),
        label="Назва вулиці",
        widget=ModelSelect2Widget(
            model=Street,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'name__iregex' ], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    # Відображається пошуковою строкою з спадаючим списком:
    oldstreetname = forms.ModelChoiceField(
        queryset=Street.objects.filter(archive=True),
        required=False, 
        # empty_label="---",
        label="Стара назва вулиці",
        widget=ModelSelect2Widget(
            model=Street,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'fullname__icontains', 'name__iregex'], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    apartmenttype = forms.ChoiceField(
        choices=apartmenttypes,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=0,
        label='Тип квартира/офіс'
    )

    class Meta:
        model = Fulladdress
        # fields = "__all__"
        fields = [
            "client",
            'addresstype',
            'index',
            'country',
            'region',
            # 'settltype',
            'cityname',
            'distr',
            # 'streettype',
            'streetname',
            'oldstreetname',
            'housenum',
            'apartmenttype',
            'apartment',
            'entrance',
            'floor',
            'comment',
        ]
        widgets = {
            # "addresstype": forms.ChoiceField(
            #     choices=addresstype,
            #     # attrs={"class": "form-control"},
            # ),
            "index": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "housenum": forms.TextInput(attrs={"class": "form-control"}),
            "apartment": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "entrance": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "floor": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

        }

