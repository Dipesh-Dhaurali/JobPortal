from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Custom filter to access dictionary items in Django templates"""
    if dictionary is None:
        return None
    return dictionary.get(key)
