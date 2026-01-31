from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit

from clients.models import Tag, Client

from libs.finances_adddata import nomenclature_type


class Nomenclature(models.Model):
    # id, name, fullname, code, type, tags, slug
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    fullname = models.CharField(max_length=255, verbose_name="Повна назва")
    code = models.IntegerField(blank=True, null=True, verbose_name="Код")
    # address = models.TextField(blank=True, verbose_name="Адреса")
    # comment = models.TextField(blank=True, verbose_name="Коммент")
    type = models.IntegerField(default=1, verbose_name="Тип", choices=nomenclature_type)
    # tags = models.ManyToManyField(Tag, blank=True, related_name="nomenclatures")
    tag = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.PROTECT, related_name="nomenclatures", verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nomenclature_detail", kwargs={"slug": self.slug})

    def get_absolute_url_for_update(self):
        return reverse("nomenclature_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("nomenclature_delete", kwargs={"slug": self.slug})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'nomenclature', "id": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "uk", reversed=True))
        super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"
        ordering = ["name"]

class Price(models.Model):
    # id, nomenclature, price, datetime
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, related_name="prices", verbose_name="Номенклатура")
    price = models.IntegerField(default=0, verbose_name="Ціна")
    datetime = models.DateTimeField(auto_now=True, verbose_name="Дата")
    # name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    # fullname = models.CharField(max_length=255, verbose_name="Повна назва")
    # code = models.IntegerField(blank=True, null=True, verbose_name="Код")
    # # address = models.TextField(blank=True, verbose_name="Адреса")
    # # comment = models.TextField(blank=True, verbose_name="Коммент")
    # type = models.IntegerField(default=1, verbose_name="Тип", choices=nomenclature_type)
    # # tags = models.ManyToManyField(Tag, blank=True, related_name="nomenclatures")
    # slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    def __str__(self):
        return self.nomenclature.name

    def get_absolute_url(self):
        return reverse("price_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("price_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("price_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'price', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Прайс"
        verbose_name_plural = "Прайси"
        ordering = ["nomenclature"]

class Balance(models.Model):
    # id, client, discount, balance
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="balance", verbose_name="Кліент")
    # discount = models.IntegerField(default=0, verbose_name="Знижка")
    balance = models.IntegerField(default=0, verbose_name="Баланс")
    datetime = models.DateTimeField(auto_now=True, verbose_name="Дата")


    def __str__(self):
        return self.client.name

    # def get_absolute_url(self):
    #     return reverse("balance_detail", kwargs={"pk": self.pk})

    # def get_absolute_url_for_update(self):
    #     return reverse("balance_update", kwargs={"pk": self.pk})

    # def get_absolute_url_for_delete(self):
    #     return reverse("balance_delete", kwargs={"pk": self.pk})
    
    # def get_absolute_url_for_logs(self):
    #     return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'balance', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Баланс"
        ordering = ["pk"]

class Discount(models.Model):
    # id, client, discount, balance
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="discount", verbose_name="Кліент")
    # discount = models.IntegerField(default=0, verbose_name="Знижка")
    discount = models.IntegerField(default=0, verbose_name="Знижка")
    datetime = models.DateTimeField(auto_now=True, verbose_name="Дата")


    def __str__(self):
        return self.client.name

    # def get_absolute_url(self):
    #     return reverse("balance_detail", kwargs={"pk": self.pk})

    # def get_absolute_url_for_update(self):
    #     return reverse("balance_update", kwargs={"pk": self.pk})

    # def get_absolute_url_for_delete(self):
    #     return reverse("balance_delete", kwargs={"pk": self.pk})
    
    # def get_absolute_url_for_logs(self):
    #     return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'balance', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Знижка"
        verbose_name_plural = "Знижки"
        ordering = ["client"]