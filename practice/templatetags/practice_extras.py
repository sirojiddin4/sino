from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary.
    Used to access user answers by question ID.
    """
    if dictionary is None:
        return None
    
    if isinstance(key, str) and key.isdigit():
        key = int(key)
    
    return dictionary.get(key)

@register.filter
def get_attribute(obj, attr):
    """
    Gets an attribute from an object.
    """
    return getattr(obj, attr, None)