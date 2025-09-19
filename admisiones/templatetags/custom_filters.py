from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Splits a string by the given key
    Usage: {{ value|split:"," }}
    """
    if value:
        return value.split(key)
    return []
