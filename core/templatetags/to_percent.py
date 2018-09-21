""" this tag joins attributes from objects inside a list """
from django import template


register = template.Library()


@register.filter
def to_percent(value, max_value):
    """ tag """
    factor = 100 / max_value if max_value else 0
    return value * factor
