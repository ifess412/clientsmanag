from django import template

# from clients.models import Tag
from libs.menu import menus, adm_menus, site_logo

# from django.urls import reverse


register = template.Library()


@register.inclusion_tag("clients/menu_tpl.html")
def show_menu(menu_class="navmenu"):
    if (menu_class =='foradmins'): 
        items = adm_menus
        mclass = "navmenu"
    else: 
        items = menus
        mclass = "navmenu"
    # tags = Tag.objects.all()
    # user_profile_url = reverse('user_profile', args=[user_id])
    return {"items": items, "menu_class": mclass}

@register.inclusion_tag("clients/logo_tpl.html")
def show_logo():
    if site_logo: 
        return {"site_name": site_logo.get('site_name'), "logo_url": site_logo.get('logo_url')}
    else: return {"site_name": "My Site", "logo_url": "/"}
