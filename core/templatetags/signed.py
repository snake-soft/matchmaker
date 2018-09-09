""" returns int or float with a sign as string """
from django import template


register = template.Library()


@register.filter
def signed(int_or_float):
    """ returns signed str """
    if not any([isinstance(int_or_float, type_) for type_ in [int, float]]):
        int_or_float = int(int_or_float)

    return '+' + str(int_or_float) if int_or_float >= 0 else str(int_or_float)
