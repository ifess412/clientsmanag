from django import template
from clients.models import Tag, City
# from clients.libs.adddata import buttons, msg
from libs.all_adddata import buttons, msg


register = template.Library()


@register.inclusion_tag("clients/add_city_tpl.html")
def add_city():
    # tags = Tag.objects.all()
    mdata = {}
    # mdata.title = 'City'
    # user_profile_url = reverse('user_profile', args=[user_id])
    return {"elems": buttons, "msg": msg, "data": mdata}
    
