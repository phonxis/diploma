from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def change_path(path):
    return "/".join(path.split('/')[2:])
