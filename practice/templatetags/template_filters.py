from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary using the key.
    Example usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)