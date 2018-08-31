from django import template


register = template.Library()


@register.filter
def attrib_get(obj, attrib):
    return getattr(obj, attrib)
