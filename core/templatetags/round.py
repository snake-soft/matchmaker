""" this tag joins attributes from objects inside a list """
from django import template


register = template.Library()


@register.filter
def round(float_, after_comma=0):
    """ tag """
    factor = 10**after_comma
    float_ = int(float_ * factor + 0.5) / factor
    return float(float_) if after_comma else int(float_)