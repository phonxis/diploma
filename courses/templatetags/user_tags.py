from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def name_of_model(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None

@register.filter(name='check_group')
def check_group(user):
	group = Group.objects.get(name='Instructor')
	return True if group in user.groups.all() else False