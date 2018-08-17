from django import template


register = template.Library()


@register.filter
def join_by_attr(the_list, attr_name, separator=', '):
    return separator.join(str(getattr(x, attr_name)) for x in the_list)
