from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from datetime import date

from clients.models import Tag, Client

# from libs.finances_adddata import nomenclature_type, paytypes, paystatuses
from libs.addata_finances import nomenclature_type, paytypes, paystatuses
# from libs.clients_adddata import client_type, app_names


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
    # price = models.IntegerField(default=0, verbose_name="Ціна")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Ціна")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
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

class Cashbook(models.Model):
    # id, num, datedoc, payer, payee, sum, paytype, paystatus, comment
    num = models.IntegerField(blank=True, null=True, verbose_name="Номер")
    datedoc = models.DateField(default=date.today, verbose_name="Дата")
    # datetime = models.DateTimeField(auto_now=True, verbose_name="Дата")
    payer = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="payercashbooks", verbose_name="Платник")
    payee = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="payeecashbooks", verbose_name="Отримувач")
    # nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, related_name="prices", verbose_name="Номенклатура")
    # sum = models.IntegerField(default=0, verbose_name="Сума")
    sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    # Лучший выбор для цен, процентов и точных значений. Требует указания max_digits (всего знаков) и decimal_places (знаков после запятой).
    paytype = models.IntegerField(default=1, verbose_name="Тип платежу", choices=paytypes)
    paystatus = models.IntegerField(default=1, verbose_name="Статус", choices=paystatuses)
    # price = models.IntegerField(default=0, verbose_name="Ціна")
    # datedoc = models.DateField(verbose_name="Дата")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар (призначення платежу)")

    def __str__(self):
        payment = ' №'+ str(self.num) + ' від ' + self.datedoc.strftime('%d.%m.%Y')
        return payment

    def get_absolute_url(self):
        return reverse("cashbook_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("cashbook_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("cashbook_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'cashbook', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Платіж"
        verbose_name_plural = "Платежі"
        ordering = ["-pk"]

class Transaction(models.Model):
    # id, client, sum, datetime, balance, docapp, docmodel, docid
    # num = models.IntegerField(blank=True, null=True, verbose_name="Номер")
    docdate = models.DateField(default = '2026-01-01',verbose_name="Дата")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="transactions", verbose_name="Client")
    # payee = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="payeecashbooks", verbose_name="Отримувач")
    # nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, related_name="prices", verbose_name="Номенклатура")
    # sum = models.IntegerField(default=0, verbose_name="Сума")
    sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sum")
    # balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="balance", default=0.00)
    # paytype = models.IntegerField(default=1, verbose_name="Тип платежу", choices=paytypes)
    # paystatus = models.IntegerField(default=1, verbose_name="Статус", choices=paystatuses)
    # price = models.IntegerField(default=0, verbose_name="Ціна")
    # datedoc = models.DateField(verbose_name="Дата")
    # comment = models.TextField(blank=True, null=True, verbose_name="Коментар (призначення платежу)")
    docapp = models.CharField(max_length=100, default='finances', verbose_name="doc_app")
    docmodel = models.CharField(max_length=100, verbose_name="doc_model")
    docid = models.IntegerField(default=0, verbose_name="doc_id")
    datetime = models.DateTimeField(auto_now=True, verbose_name="Date time")

    def __str__(self):
        strmodelname = ' №'+ str(self.pk) + ' від ' + self.datetime.strftime('%d.%m.%Y')
        return strmodelname
        # return self.pk

    def get_absolute_url(self):
        return reverse("transaction_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("transaction_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("transaction_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'transaction', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Операція"
        verbose_name_plural = "Операції"
        ordering = ["-pk"]

class License(models.Model):
    # id, num, client, nomenclature, price, orderdate, enddate, pccode, licensecode, seller, 
    # developer, devdiscount, devprice, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment
    num = models.IntegerField(blank=True, null=True, verbose_name="Номер")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="clientlicenses", verbose_name="Кліент")
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, related_name="licenses", verbose_name="Ліцензія")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Ціна")
    # orderdate = models.DateField(default = '2026-01-01', verbose_name="orderdate")
    orderdate = models.DateField(default=date.today, verbose_name="Дата замовлення")
    enddate = models.DateField(verbose_name="Дата закінчення")
    pccode = models.CharField(blank=True, null=True, max_length=100, verbose_name="Код компьютера")
    licensecode = models.CharField(blank=True, null=True, max_length=255, verbose_name="Код ліцензії")
    seller = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="sellerlicenses", verbose_name="Постачальник")
    developer = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="developerlicenses", verbose_name="Розробник")
    devdiscount =  models.IntegerField(default=0, verbose_name="Відсоток Розробника")
    devprice = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Оплата Розробнику")
    agent = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="agentlicenses", verbose_name="Агент")
    agdiscount =  models.IntegerField(default=0, verbose_name="Відсоток Агента")
    agprice = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Оплата Агенту")
    taxes = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="taxeslicenses", verbose_name="Податки")
    taxdiscount =  models.IntegerField(default=0, verbose_name="Відсоток Податку")
    taxprice = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Оплата Податку")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")

    def __str__(self):
        if (self.num):
            lic = ' №'+ str(self.num) + ' від ' + self.orderdate.strftime('%d.%m.%Y')
        else:
            lic = ' ID'+ str(self.num) + ' від ' + self.orderdate.strftime('%d.%m.%Y')
        return lic

    def get_absolute_url(self):
        return reverse("license_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("license_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("license_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'license', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Ліцензія"
        verbose_name_plural = "Ліцензії"
        ordering = ["enddate"]

class Act(models.Model):
    # id, num, datedoc, client, nomenclature, price, seller, agent, agdiscount, agprice, taxes, taxdiscount, taxprice, comment
    num = models.IntegerField(blank=True, null=True, verbose_name="Номер")
    datedoc = models.DateField(default=date.today, verbose_name="Дата")
    # provider = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="provideracts", verbose_name="Виконавець")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="clientacts", verbose_name="Замовник")
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.PROTECT, related_name="nomenclatureacts", verbose_name="Послуга")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Ціна")
    # sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    # Лучший выбор для цен, процентов и точных значений. Требует указания max_digits (всего знаков) и decimal_places (знаков после запятой).
    # paytype = models.IntegerField(default=1, verbose_name="Тип платежу", choices=paytypes)
    # paystatus = models.IntegerField(default=1, verbose_name="Статус", choices=paystatuses)
    seller = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True, related_name="selleracts", verbose_name="Виконавець")
    # developer = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="developerlicenses", verbose_name="Розробник")
    # devdiscount =  models.IntegerField(default=0, verbose_name="Відсоток Розробника")
    # devprice = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Оплата Розробнику")
    agent = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True, related_name="agentacts", verbose_name="Підрядник")
    agdiscount =  models.IntegerField(default=0, verbose_name="Відсоток Підрядник")
    agprice = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Оплата Підрядник")
    taxes = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True, related_name="taxesacts", verbose_name="Податки")
    taxdiscount =  models.IntegerField(default=0, verbose_name="Відсоток Податку")
    taxprice = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Оплата Податку")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")

    def __str__(self):
        # f-строки работают быстрее и читаются проще
        date_str = self.datedoc.strftime('%d.%m.%Y')
        if self.num:
            return f"Акт №{self.num} від {date_str}"
        # Исправлено: если номера нет, выводим ID записи (self.pk или self.id)
        return f"Акт ID{self.pk} від {date_str}"

    def get_absolute_url(self):
        return reverse("act_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("act_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("act_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'finances', "mdl": 'act', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Акт"
        verbose_name_plural = "Акти"
        ordering = ["-datedoc"]
