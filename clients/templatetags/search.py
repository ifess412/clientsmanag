from django import template
from clients.models import Tag, Client, Access, Contact
# from clients.libs.adddata import buttons, msg
from libs.all_adddata import buttons, msg


register = template.Library()


@register.inclusion_tag("clients/search_tpl.html")
def search_field(table="clients"):
    # tags = Tag.objects.all()
    # user_profile_url = reverse('user_profile', args=[user_id])
    return {"elems": buttons, "msg": msg, "table": table}
    # return {"table": table}
