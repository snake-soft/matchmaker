""" tag that returns attribute from object """
from django import template


register = template.Library()


@register.filter
def attrib_get(obj, attrib):
    """ returns attribute """
    return getattr(obj, attrib)
