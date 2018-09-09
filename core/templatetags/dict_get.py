""" filter (pipeable) """
from django import template


register = template.Library()


@register.filter
def dict_get(the_dict, key):
    """ get value from dict """
    return the_dict[key]
