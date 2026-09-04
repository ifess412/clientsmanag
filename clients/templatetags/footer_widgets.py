from django import template

# from clients.models import Tag
# from libs.settings import site_name
from libs.footer import *

# from django.urls import reverse

register = template.Library()

@register.inclusion_tag("clients/footer_widget_menu_tpl.html")
def footer_widget_menu(widget="useful links"):
    if (widget =='useful_links'): 
        items = useful_links
        widget_title = useful_links_title 
    elif (widget =='our_services'):
        items = our_services
        widget_title = our_services_title 
    return {"items": items, "widget_title": widget_title}

@register.inclusion_tag("clients/footer_widget_html_tpl.html")
def footer_widget_html(widget="about"):
    if (widget =='about'): 
        html_code = footer_about
    elif (widget =='follow_us'): 
        html_code = footer_folow_us
    elif (widget =='copyright'): 
        html_code = footer_copyright
    else:
        html_code = False
    return {"html_code": html_code}



