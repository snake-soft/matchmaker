""" get element from list (pipeable) """
from django import template


register = template.Library()


@register.filter
def list_get(the_list, index):
    """ get element from dict """
    return the_list[index]
