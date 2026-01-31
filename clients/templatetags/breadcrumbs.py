from django import template

# from clients.models import Client, Tag

register = template.Library()


@register.inclusion_tag("clients/breadcrumbs_tpl.html")
def show_breadcrumps(title="Home"):
    # tags = Tag.objects.all()
    bcs = (
        {"title": "Головна", "url": "/"},
        {"title": "Клієнти", "url": "/clients"},
    )
    last_element = bcs[-1]
    title = last_element["title"]
    return {"bcs": bcs, "title": title}
