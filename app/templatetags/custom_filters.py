from django import template

register = template.Library()

@register.filter
def split(value, delimiter=";"):
    """Divide uma string pelo delimitador especificado."""
    return value.split(delimiter)