from django import template


register = template.Library()


@register.filter
def list_get(the_list, index):
    return the_list[index]
