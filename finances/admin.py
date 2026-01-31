from django.contrib import admin

from .models import *
from libs.finances_adddata import nomenclature_type



class NomenclatureAdmin(admin.ModelAdmin):
    # id, name, fullname, code, type, tags, slug
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ("id", "name", "fullname", "code", "type", "slug")
    list_display_links = ("id", "name")
    search_fields = ("name", "fullname", "code")
    list_filter = ("tag",)
    readonly_fields = ("c_type",) 
    fields = (
        "name",
        "fullname",
        "code",
        # "address",
        # "comment",
        "type",
        "tag",
        # "c_type",
        "slug",
    )

    def c_type(self, obj):
        if obj.type:
            return nomenclature_type[obj.type]
        return "-"

    c_type.short_description = "Тип"

class PriceAdmin(admin.ModelAdmin):
    # id, nomenclature, price, datetime
    # prepopulated_fields = {"id": ("id",)}
    prepopulated_fields = {"id": ("id",)}
    save_on_top = True
    list_display = ("id", "nomenclature", "price", "datetime")
    list_display_links = ("id", "nomenclature")
    search_fields = ("nomenclature",)
    list_filter = ("nomenclature",)
    # readonly_fields = ("id","datetime",) 
    # fields = (
    #     "id",
    #     "nomenclature",
    #     "price",
    #     # "datetime",
    # )

    # def c_type(self, obj):
    #     if obj.type:
    #         return nomenclature_type[obj.type]
    #     return "-"

    # c_type.short_description = "Тип"    


admin.site.register(Nomenclature, NomenclatureAdmin)
# admin.site.register(Price, PriceAdmin)
admin.site.register(Price)
admin.site.register(Discount)


