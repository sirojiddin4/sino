from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary using the key.
    Example usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def split_answer(answer_string):
    """
    Splits a comma-separated answer string into a list.
    Example usage: {{ answer_string|split_answer }}
    """
    if not answer_string:
        return []
    return [item.strip() for item in answer_string.split(',')]

@register.filter
def contains(list_obj, value):
    """
    Checks if a list contains a value.
    Example usage: {{ list|contains:value }}
    """
    return value in list_obj