from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget
# from django_select2 import forms as s2forms
# from django.core.validators import RegexValidator
# import re
# from django.core.exceptions import ValidationError

from .models import Nomenclature, Price, Client, Discount

# from libs.finances_tableheads import *
# from libs.finances_adddata import *
# from libs.settings import *

class NomenclatureForm(forms.ModelForm):
    # id, name, fullname, code, type, tags, slug
    class Meta:
        model = Nomenclature
        # fields = "__all__"
        fields = [
            "name",
            "fullname",
            "code",
            # "address",
            # "comment",
            "type",
            "tag",
            # "slug",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
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

    # def clean_title(self):
    #     title = self.cleaned_data["title"]
    #     if re.match(r"\d", title):
    #         raise ValidationError("Название не должно начинаться с цифры")
    #     return title
        
class PriceForm(forms.ModelForm):
    # id, name, fullname, code, type, tags, slug

    # Номенклатура відображається спадаючим списком:
    # nomenclature = forms.ModelChoiceField(
    #     queryset=Nomenclature.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-control"}), 
    #     label="Номенклатура")

    # Номенклатура відображається пошуковою строкою з спадаючим списком:
    nomenclature = forms.ModelChoiceField(
        queryset=Nomenclature.objects.all(),
        label="Номенклатура",
        widget=ModelSelect2Widget(
            model=Nomenclature,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'fullname__icontains', 'code__icontains'], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    
    class Meta:
        model = Price
        # fields = "__all__"
        fields = [
            "nomenclature",
            "price",
            # "date_time",
        ]
        widgets = {
            "price": forms.TextInput(attrs={"class": "form-control"}),
        }

class DiscountForm(forms.ModelForm):
    # id, name, fullname, code, type, tags, slug

    # Номенклатура відображається спадаючим списком:
    # client = forms.ModelChoiceField(
    #     queryset=Client.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-control"}), 
    #     label="Номенклатура")

    # Номенклатура відображається пошуковою строкою з спадаючим списком:
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Клієнт",
        widget=ModelSelect2Widget(
            model=Client,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'fullname__icontains', 'code__icontains'], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    
    class Meta:
        model = Discount
        # fields = "__all__"
        fields = [
            "client",
            "discount",
            # "date_time",
        ]
        widgets = {
            "discount": forms.TextInput(attrs={"class": "form-control"}),
        }
        
