from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget
# from django_select2 import forms as s2forms
# from django.core.validators import RegexValidator
# import re
# from django.core.exceptions import ValidationError

from .models import *
# from libs.finances_adddata import nomenclature_type, paytypes, paystatuses
from libs.addata_finances import nomenclature_type, paytypes, paystatuses

# from libs.finances_tableheads import *
# from libs.finances_adddata import *
# from libs.settings import *

class NomenclatureForm(forms.ModelForm):
    # id, name, fullname, code, type, tags, slug
    type = forms.ChoiceField(
        choices=nomenclature_type,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=1,
        label='Тип'
    )
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.CheckboxSelectMultiple, 
    #     label="Теги"
    # )
    # Відображається спадаючим списком:
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Тег")

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
        
class BalanceForm(forms.ModelForm):
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
        model = Balance
        # fields = "__all__"
        fields = [
            "client",
            "balance",
            # "date_time",
        ]
        widgets = {
            "balance": forms.TextInput(attrs={"class": "form-control"}),
        }
        
class CashbookForm(forms.ModelForm):
    # id, num, datedoc, payer, payee, sum, paytype, paystatus, comment
    
    paytype = forms.ChoiceField(
        choices=paytypes,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=0,
        label='Тип'
    )
    paystatus = forms.ChoiceField(
        choices=paystatuses,
        widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
        initial=0,
        label='Статус'
    )
    # Відображається спадаючим списком:
    # tags = forms.ModelChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-control"}), 
    #     label="Теги")
    
    # Відображається пошуковою строкою з спадаючим списком:
    payer = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Платник",
        widget=ModelSelect2Widget(
            model=Client,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'name__iregex' ], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    # Відображається пошуковою строкою з спадаючим списком:
    payee = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Отримувач",
        widget=ModelSelect2Widget(
            model=Client,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'name__iregex' ], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    sum = forms.DecimalField(
        label="Сума",
        min_value=0, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
    datedoc = forms.DateField(
        label="Дата",
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={"class": "form-control", 'type': 'date'
            }
        )
    )
        
    class Meta:
        model = Cashbook
        # fields = "__all__"
        fields = [
            'num',
            "datedoc",
            "payer",
            "payee",
            "sum",
            "paytype",
            "paystatus",
            "comment",
        ]
        widgets = {
            # "num": forms.TextInput(attrs={"class": "form-control"}),
            # "num": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "num": forms.TextInput(attrs={"data-model":"cashbook","class": "form-control", "type":"number"}),
            # "sum": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class LicenseForm(forms.ModelForm):
    # id, num, client, nomenclature, price, orderdate, enddate, pccode, licensecode, seller, 
    # developer, devdiscount, devprice, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment

    # paystatus = forms.ChoiceField(
    #     choices=paystatuses,
    #     widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
    #     initial=0,
    #     label='Статус'
    # )
    # Відображається спадаючим списком:
    # tags = forms.ModelChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.Select(attrs={"class": "form-control"}), 
    #     label="Теги")
    
    # Відображається пошуковою строкою з спадаючим списком:
    client = forms.ModelChoiceField(
        # queryset=Client.objects.all(),
        queryset=Client.objects.filter(type=1),
        label="Кліент",
        widget=ModelSelect2Widget(
            model=Client,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'name__iregex' ], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    # Відображається спадаючим списком:
    nomenclature = forms.ModelChoiceField(
        queryset=Nomenclature.objects.filter(type=1), #обираемо номенклатуру с типом ліцензія
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Ліцензія",
    )
    # # Відображається пошуковою строкою з спадаючим списком:
    # nomenclature = forms.ModelChoiceField(
    #     # queryset=Nomenclature.objects.all(),
    #     queryset=Nomenclature.objects.filter(type=1), #обираемо номенклатуру с типом ліцензія
    #     label="Ліцензія",
    #     widget=ModelSelect2Widget(
    #         model=Nomenclature,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', 'name__iregex'], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    # Відображається спадаючим списком:
    seller = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=0),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Постачальник",
        )
    # Відображається пошуковою строкою з спадаючим списком:
    # seller = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.filter(type=0),
    #     label="Постачальник",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    price = forms.DecimalField(
        label="Ціна",
        min_value=0, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
    orderdate = forms.DateField(
        label="Дата замовлення",
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={"class": "form-control", 'type': 'date'
            }
        )
    )
    enddate = forms.DateField(
        label="Дата закінчення",
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={"class": "form-control", 'type': 'date'
            }
        )
    )
    # Відображається спадаючим списком:
    developer = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=2),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Розробник",
        )
    # Відображається пошуковою строкою з спадаючим списком:
    # developer = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.filter(type=2),
    #     label="Розробник",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    devdiscount = forms.IntegerField(
        label="Відсоток Розробника",
        initial=0,
        min_value=0, # Optional: set minimum value
        max_value=100, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "1" # Optional: allows two decimal places
            }
        )
    )
    devprice = forms.DecimalField(
        label="Оплата Розробнику",
        initial=0,
        min_value=0, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
    # Відображається спадаючим списком:
    agent = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=2),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Агент",
        )
    # # Відображається пошуковою строкою з спадаючим списком:
    # agent = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.filter(type=2),
    #     label="Агент",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    agdiscount = forms.IntegerField(
        label="Відсоток Агента",
        initial=0,
        min_value=-100, # Optional: set minimum value
        max_value=100, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "1" # Optional: allows two decimal places
            }
        )
    )
    agprice = forms.DecimalField(
        label="Оплата Агенту",
        initial=0,
        # min_value=0, 
        # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
    # Відображається спадаючим списком:
    taxes = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=2),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Податки",
        )
    # # Відображається пошуковою строкою з спадаючим списком:
    # taxes = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.filter(type=2),
    #     label="Податки",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    taxdiscount = forms.IntegerField(
        label="Відсоток Податку",
        initial=0,
        min_value=0, # Optional: set minimum value
        max_value=100, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "1" # Optional: allows two decimal places
            }
        )
    )
    taxprice = forms.DecimalField(
        label="Оплата Податку",
        initial=0,
        min_value=0, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
        
    class Meta:
        model = License
        # fields = "__all__"
        fields = [
            'num',
            "client",
            "nomenclature",
            "price",
            "orderdate",
            "enddate",
            "pccode",
            "licensecode",
            "seller",
            "developer",
            "devdiscount",
            "devprice",
            "agent",
            "agdiscount",
            "agprice",
            "taxes",
            "taxdiscount",
            "taxprice",
            "comment",
        ]
        widgets = {
            # "num": forms.TextInput(attrs={"class": "form-control"}),
            "num": forms.TextInput(attrs={"data-model":"license","class": "form-control", "type":"number"}),
            "pccode": forms.TextInput(attrs={"class": "form-control"}),
            "licensecode": forms.TextInput(attrs={"class": "form-control"}),
            # "sum": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class ActForm(forms.ModelForm):
    # id, num, datedoc, client, nomenclature, price, seller, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment
    datedoc = forms.DateField(
        label="Дата",
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={"class": "form-control", 'type': 'date'
            }
        )
    )
    # Відображається пошуковою строкою з спадаючим списком:
    # provider = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.all(),
    #     # queryset=Client.objects.filter(type=2),
    #     # queryset=Client.objects.filter(type=0),
    #     label="Кліент",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', 'name__iregex' ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    
    # Відображається пошуковою строкою з спадаючим списком:
    client = forms.ModelChoiceField(
        # queryset=Client.objects.all(),
        queryset=Client.objects.filter(type=1),
        label="Кліент",
        widget=ModelSelect2Widget(
            model=Client,
            # search_fields=['name__icontains'], 
            search_fields=['name__icontains', 'name__iregex' ], 
            attrs={"class": "form-control",
                #    "value": self.i,
                   }
            )
        )
    # Відображається спадаючим списком:
    nomenclature = forms.ModelChoiceField(
        # queryset=Nomenclature.objects.filter(type=1), #обираемо номенклатуру с типом ліцензія
        # queryset=Nomenclature.objects.filter(type=2), #обираемо номенклатуру с типом ліцензія
        queryset=Nomenclature.objects.all(), #обираемо номенклатуру всю
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Послуга",
    )
    # # Відображається пошуковою строкою з спадаючим списком:
    # nomenclature = forms.ModelChoiceField(
    #     # queryset=Nomenclature.objects.all(),
    #     queryset=Nomenclature.objects.filter(type=1), #обираемо номенклатуру с типом ліцензія
    #     label="Ліцензія",
    #     widget=ModelSelect2Widget(
    #         model=Nomenclature,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', 'name__iregex'], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    
    price = forms.DecimalField(
        label="Ціна",
        min_value=0, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
    # paytype = forms.ChoiceField(
    #     choices=paytypes,
    #     widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
    #     initial=0,
    #     label='Тип'
    # )
    # paystatus = forms.ChoiceField(
    #     choices=paystatuses,
    #     widget=forms.Select(attrs={'class': 'form-control', 'data-info': 'some-data'}),
    #     initial=0,
    #     label='Статус'
    # )
    # Відображається спадаючим списком:
    seller = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=0),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Виконавець",
        )
    # Відображається спадаючим списком:
    agent = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=2),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Підрядник",
        )
    # # Відображається пошуковою строкою з спадаючим списком:
    # agent = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.filter(type=2),
    #     label="Агент",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    agdiscount = forms.IntegerField(
        label="Відсоток Підрядник",
        initial=0,
        min_value=-100, # Optional: set minimum value
        max_value=100, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "1" # Optional: allows two decimal places
            }
        )
    )
    agprice = forms.DecimalField(
        label="Оплата Підрядник",
        initial=0,
        # min_value=0, 
        # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
    # Відображається спадаючим списком:
    taxes = forms.ModelChoiceField(
        queryset=Client.objects.filter(type=2),
        widget=forms.Select(attrs={"class": "form-control"}), 
        label="Податки",
        )
    # # Відображається пошуковою строкою з спадаючим списком:
    # taxes = forms.ModelChoiceField(
    #     # queryset=Client.objects.all(),
    #     queryset=Client.objects.filter(type=2),
    #     label="Податки",
    #     widget=ModelSelect2Widget(
    #         model=Client,
    #         # search_fields=['name__icontains'], 
    #         search_fields=['name__icontains', ], 
    #         attrs={"class": "form-control",
    #             #    "value": self.i,
    #                }
    #         )
    #     )
    taxdiscount = forms.IntegerField(
        label="Відсоток Податку",
        initial=0,
        min_value=0, # Optional: set minimum value
        max_value=100, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "1" # Optional: allows two decimal places
            }
        )
    )
    taxprice = forms.DecimalField(
        label="Оплата Податку",
        initial=0,
        min_value=0, # Optional: set minimum value
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "step": "0.01" # Optional: allows two decimal places
            }
        )
    )
            
    class Meta:
        model = Act
        # fields = "__all__"
        fields = [
            'num',
            "datedoc",
            # "provider",
            "client",
            "nomenclature",
            "price",
            # "paytype",
            # "paystatus",
            "seller",
            "agent",
            "agdiscount",
            "agprice",
            "taxes",
            "taxdiscount",
            "taxprice",
             "comment",
        ]
        widgets = {
            # "num": forms.TextInput(attrs={"class": "form-control"}),
            "num": forms.TextInput(attrs={"data-model":"act","class": "form-control", "type":"number"}),
            # "pccode": forms.TextInput(attrs={"class": "form-control"}),
            # "licensecode": forms.TextInput(attrs={"class": "form-control"}),
            # "sum": forms.TextInput(attrs={"class": "form-control", "type":"number"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

