from django import template


register = template.Library()


@register.filter
def dict_get(the_dict, key):
    return the_dict[key]
