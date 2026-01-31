from django.contrib import admin
from .models import *
from libs.clients_adddata import client_type

# Models:
# Tag
# Client
# Access
# Contact
# Add_data


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    # list_filter = ("category",)
    # readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ("title", "slug")


class ClientAdmin(admin.ModelAdmin):
    # id, name, fullname, code, address, comment, type, slug
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ("id", "name", "fullname", "code", "type", "slug")
    # list_display = ("id", "name", "fullname", "code", "c_type")
    list_display_links = ("id", "name")
    search_fields = ("name", "fullname", "code")
    list_filter = ("tags",)
    readonly_fields = ("c_type",)
    fields = (
        "name",
        "fullname",
        "code",
        "address",
        "comment",
        "type",
        # "c_type",
        "slug",
    )

    def c_type(self, obj):
        if obj.type:
            return client_type[obj.type]
        return "-"

    c_type.short_description = "Тип"


class AccessAdmin(admin.ModelAdmin):
    # id, name, app, idinapp, passinapp, comment, client, order, slug
    prepopulated_fields = {"slug": ("name", "app")}
    save_on_top = True
    list_display = ("id", "name", "app", "client")
    # list_display = ("id", "name", "app", "idinapp", "passinapp", "client")
    list_display_links = ("id", "name")
    search_fields = ("name", "app", "idinapp", "comment", "client")
    list_filter = ("client",)
    # # readonly_fields = ('views', 'created_at', 'get_photo')
    # fields = ("title", "slug")


class ContactAdmin(admin.ModelAdmin):
    # id, name, phone1, phone2, phone3, email, comment, client, position, order, slug
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    list_display = ("id", "name", "phone1", "phone2", "email", "client")
    list_display_links = ("id", "name")
    search_fields = ("name", "phone1", "phone2", "phone3", "email")
    list_filter = ("client",)
    # # readonly_fields = ('views', 'created_at', 'get_photo')
    # fields = ("title", "slug")


# class PostAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}
#     form = PostAdminForm
#     save_as = True
#     save_on_top = True
#     list_display = ('id', 'title', 'slug', 'category', 'created_at', 'get_photo')
#     list_display_links = ('id', 'title')
#     search_fields = ('title',)
#     list_filter = ('category',)
#     readonly_fields = ('views', 'created_at', 'get_photo')
#     fields = ('title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at')

#     def get_photo(self, obj):
#         if obj.photo:
#             return mark_safe(f'<img src="{obj.photo.url}" width="50">')
#         return '-'

#     get_photo.short_description = 'Фото'


admin.site.register(Tag, TagAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(City)
admin.site.register(Distr)
admin.site.register(Street)
admin.site.register(Fulladdress)
