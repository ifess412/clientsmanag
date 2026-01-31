from django.db import models
# from phone_field import PhoneField
# from django.core.validators import RegexValidator
from django.urls import reverse
# from django.utils.text import slugify
# from transliterate import translit
from django.contrib.auth import get_user_model

    

from libs.logs_adddata import action_tag


class Islog(models.Model):
    # id, app_label, obj_model, obj_id, mess, action_tag, user_id, date_time
    app_label = models.CharField(max_length=100, default='clients', verbose_name="app_label")
    obj_model = models.CharField(max_length=100, verbose_name="obj_model")
    obj_id = models.IntegerField(default=0, verbose_name="obj_id")
    mess = models.TextField(blank=True)
    action_tag = models.IntegerField(default=0, verbose_name="action_tag", choices=action_tag)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mess

    # def get_absolute_url(self):
    #     return reverse("access_detail", kwargs={"slug": self.slug})

    # def get_absolute_url_for_update(self):
    #     return reverse("access_update", kwargs={"slug": self.slug})

    def get_absolute_url_for_delete(self):
        return reverse("islog_delete", kwargs={"pk": self.pk})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.name, "uk", reversed=True))
    #     super(Access, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ["date_time"]


