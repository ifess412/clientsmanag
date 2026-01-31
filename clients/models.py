from django.db import models
# from phone_field import PhoneField
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
# from django.contrib.auth import get_user_model

    

# from clients.libs.adddata import client_type, app_names
from libs.clients_adddata import client_type, app_names
from libs.add_address import addresstypes, countries, regions, settltypes, streettypes, apartmenttypes


"""
Models:
Tag 
Client 
Access
Contact
Add_data

"""


# def gen_slug(string):
#     finally_slug = slugify(string)
#     # finally_slug = slugify(string, allow_unicode=True)
#     return finally_slug + "-" + str(int(time()))


class Tag(models.Model):
    # id, title, color, slug
    title = models.CharField(max_length=50, unique=True, verbose_name="Назва")
    color = models.CharField(max_length=100, blank=True,  verbose_name="Колір")
    slug = models.SlugField(max_length=50, verbose_name="Url", unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tag_detail", kwargs={"slug": self.slug})

    def get_absolute_url_for_filter(self):
        return reverse("filterbytag", kwargs={"slug": self.slug})

    def get_absolute_url_for_update(self):
        return reverse("tag_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("tag_delete", kwargs={"slug": self.slug})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'tag', "id": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, "uk", reversed=True))
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["title"]

class Client(models.Model):
    # id, name, fullname, code, address, comment, type, tags, slug
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва клієнта")
    fullname = models.CharField(max_length=255, verbose_name="Повна назва клієнта")
    code = models.IntegerField(blank=True,  null=True, verbose_name="Код ЄДРПОУ")
    address = models.TextField(blank=True,  null=True, verbose_name="Адреса")
    comment = models.TextField(blank=True, null=True, verbose_name="Коммент")
    type = models.IntegerField(default=1, verbose_name="Тип", choices=client_type)
    tags = models.ManyToManyField(Tag, blank=True, related_name="clients")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("client_detail", kwargs={"slug": self.slug})

    def get_absolute_url_for_update(self):
        return reverse("client_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("client_delete", kwargs={"slug": self.slug})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'client', "id": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "uk", reversed=True))
        super(Client, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
        ordering = ["-pk"]

class Access(models.Model):
    # id, name, app, idinapp, passinapp, comment, client, order, slug
    name = models.CharField(max_length=100, verbose_name="Назва компа")
    app = models.CharField(
        max_length=100, verbose_name="Застосунок для доступу", choices=app_names
    )
    # app = models.IntegerField(default=0)
    idinapp = models.CharField(
        blank=True, max_length=100, verbose_name="ID в застосунку"
    )
    passinapp = models.CharField(blank=True, max_length=255, verbose_name="Пароль")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="accesses", verbose_name="Клієнт")
    order = models.IntegerField(default=1, verbose_name="Порядок")
    comment = models.TextField(blank=True, verbose_name="Коммент")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("access_detail", kwargs={"slug": self.slug})

    def get_absolute_url_for_update(self):
        return reverse("access_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("access_delete", kwargs={"slug": self.slug})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'access', "id": self.pk})    

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "uk", reversed=True))
        # if self.pk is None:
        #     usr = request.user
        #     print(usr)
        #     usrid = usr.id
        #     print(usrid)
        #     new=Islog.objects.create(obj_model='clients_client', obj_id='3', action_tag='1', mess='123', user_id=usrid)
        #     print(new.pk)
        # else:
        #     pass
        super(Access, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Доступ"
        verbose_name_plural = "Доступи"
        ordering = ["name"]

class Contact(models.Model):
    # id, name, phone1, phone2, phone3, email, comment, client, position, order, slug
    phonevalidator = RegexValidator(
        regex=r"^\+?\d{1,4}?\s?\d{1,14}\s?\d{1,14}$",
        message="Вкажіть контактний телефон у форматі +380 XX XXX-XX-XX",
        code="invalid_phone_number",
    )
    name = models.CharField(max_length=100, unique=True, verbose_name="ПІБ")
    phone1 = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phonevalidator],
        verbose_name="Телефон 1",
    )
    phone2 = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phonevalidator],
        verbose_name="Телефон 2",
    )
    phone3 = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phonevalidator],
        verbose_name="Телефон 3",
        # help_text="Вкажіть контактний телефон у форматі (415) 123-4567.",
    )
    # phone1 = PhoneField(
    #     blank=True, help_text="Вкажіть контактний телефон у форматі (415) 123-4567. "
    # )
    email = models.EmailField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="contacts", verbose_name="Клієнт")
    position = models.CharField(max_length=100, blank=True, verbose_name="Посада")
    order = models.IntegerField(default=1, verbose_name="Порядок показу")
    comment = models.TextField(blank=True, verbose_name="Коммент")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"slug": self.slug})

    def get_absolute_url_for_update(self):
        return reverse("contact_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("contact_delete", kwargs={"slug": self.slug})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'contact', "id": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "uk", reversed=True))
        super(Contact, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакти"
        ordering = ["name"]

    # author = models.CharField(max_length=100)
    # content = models.TextField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    # photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    # views = models.IntegerField(default=0, verbose_name="Кол-во просмотров")
    # category = models.ForeignKey(
    #     Category, on_delete=models.PROTECT, related_name="posts"
    # )
    # tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    # phone1 = models.CharField(
    #     max_length=15,
    #     blank=True,
    #     null=True,
    #     validators=[
    #         RegexValidator(
    #             regex=r"^\+?\d{1,4}?\s?\d{1,14}\s?\d{1,14}$",
    #             message="Введите номер телефона в формате +ХХХ XX XXX-XX-XX",
    #             code="invalid_phone_number",
    #         )
    #     ],
    # )
        
# Далі моделі для повної адреси
class City(models.Model):
    # city
    # id, name, slug
    settltype = models.IntegerField(blank=True, null=True, verbose_name="Тип населенного пункту", choices=settltypes)
    name = models.CharField(max_length=150, unique=True, verbose_name="Назва міста/села")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("city_detail", kwargs={"slug": self.slug})

    def get_absolute_url_for_update(self):
        return reverse("city_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("city_delete", kwargs={"slug": self.slug})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'city', "id": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, "uk", reversed=True))
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Місто"
        verbose_name_plural = "Міста"
        ordering = ["name"]

class Distr(models.Model):
    # city​​distr
    # id, name,
    name = models.CharField(max_length=200, unique=True, verbose_name="Назва района міста")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("distr_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("distr_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("distr_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'distr', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Район міста"
        verbose_name_plural = "Райони міста"
        ordering = ["name"]
        
class Street(models.Model):
    # street
    # id, name, fullname, city​​distr, archive
    streettype = models.IntegerField(blank=True, null=True, verbose_name="Тип вулиці", choices=streettypes)
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    # fullname = models.CharField(max_length=255, verbose_name="Повна назва")
    distr = models.ForeignKey(Distr, blank=True, null=True, on_delete=models.PROTECT, related_name="streets", verbose_name="Район міста")
    archive = models.BooleanField(default=False, verbose_name="Архівний")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("street_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("street_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("street_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'street', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Вулиця"
        verbose_name_plural = "Вулиці"
        ordering = ["name"]

class Fulladdress(models.Model):
    # fulladdress
    # client, addresstype, index, country, region, settltype, cityname, ​​distr, streettype, streetname, oldstreetname, housenum, apartmenttype, apartment, entrance, floor, comment
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="fulladdresses", verbose_name="Клієнт")
    addresstype = models.IntegerField(default=1, verbose_name="Тип адреси", choices=addresstypes)
    index = models.IntegerField(blank=True, null=True, verbose_name="Індекс")
    country = models.IntegerField(default=1, verbose_name="Країна", choices=countries)
    region = models.IntegerField(blank=True, null=True, verbose_name="Область", choices=regions)
    # settltype = models.IntegerField(blank=True, null=True, verbose_name="Тип населенного пункту", choices=settltypes)
    cityname = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT, related_name="fulladdress", verbose_name="Назва міста/села")
    distr = models.ForeignKey(Distr, blank=True, null=True, on_delete=models.PROTECT, related_name="fulladdress", verbose_name="Район міста")
    # streettype = models.IntegerField(blank=True, null=True, verbose_name="Тип вулиці", choices=streettypes)
    streetname = models.ForeignKey(Street, on_delete=models.PROTECT, related_name="addresses", verbose_name="Назва вулиці")
    oldstreetname = models.ForeignKey(Street, blank=True, null=True, on_delete=models.PROTECT, related_name="fulladdress", verbose_name="Стара назва вулиці")
    housenum = models.CharField(max_length=10, blank=True, verbose_name="Номер будиноку")
    apartmenttype = models.IntegerField(blank=True, null=True, verbose_name="тип квартира/офіс", choices=apartmenttypes)
    apartment = models.IntegerField(blank=True, null=True, verbose_name="Номер квартири")
    entrance = models.IntegerField(blank=True, null=True, verbose_name="Під'їзд")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Поверх")
    comment = models.TextField(blank=True, null=True, verbose_name="Коммент")

    
    def __str__(self):
        title = ''
        if self.streetname: 
            if self.streetname.streettype:
                st =  self.streetname.streettype
                if st in streettypes: 
                    title += streettypes[st]
            title += self.streetname.name 
            if self.housenum:
                title += " " + str(self.housenum)
            if self.apartment:
                title += " " + str(self.apartment)
        else: title += '--'
        return title

    def get_absolute_url(self):
        return reverse("fulladdress_detail", kwargs={"pk": self.pk})

    def get_absolute_url_for_update(self):
        return reverse("fulladdress_update", kwargs={"pk": self.pk})

    def get_absolute_url_for_delete(self):
        return reverse("fulladdress_delete", kwargs={"pk": self.pk})
    
    def get_absolute_url_for_logs(self):
        return reverse("filter_islog_list", kwargs={"app": 'clients', "mdl": 'fulladdress', "id": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Nomenclature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Адреса"
        verbose_name_plural = "Адреси"
        ordering = ["streetname"]  
