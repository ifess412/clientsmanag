from django import template
from clients.models import Tag, City


register = template.Library()


@register.inclusion_tag("clients/filter_tpl.html")
def filter_tags():
    tags = Tag.objects.all()
    # user_profile_url = reverse('user_profile', args=[user_id])
    return {
        "tags": tags,
    }


