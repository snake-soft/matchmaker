from django import template


register = template.Library()


@register.filter
def signed(int_or_float):
    if not type(int_or_float) in [int, float]:
        int_or_float = int(int_or_float)
    if int_or_float >= 0:
        return '+' + str(int_or_float)
    else:
        return str(int_or_float)
