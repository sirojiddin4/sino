from django import template
import csv
import re
from io import StringIO

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

@register.filter
def filter_by_range(queryset, arg):
    """
    Filter a queryset by a range of values for a specific field.
    Usage: queryset|filter_by_range:'field_name,min,max'
    """
    args = arg.split(',')
    field_name = args[0]
    min_value = int(args[1])
    max_value = int(args[2])
    
    filter_kwargs = {
        f"{field_name}__gte": min_value,
        f"{field_name}__lte": max_value
    }
    
    return queryset.filter(**filter_kwargs).order_by(field_name)

@register.filter
def get_attr(obj, attr):
    """
    Get an attribute from an object.
    Usage: {{ object|get_attr:'attribute_name' }}
    """
    if obj is None:
        return None
    
    return getattr(obj, attr, None)

@register.filter
def filter_by_group(queryset, group):
    """
    Filter a queryset by a question group.
    Usage: queryset|filter_by_group:group
    """
    if not group:
        return queryset.none()
    
    return queryset.filter(question_group=group).order_by('order_number')

@register.filter
def parse_csv_table(csv_text):
    """
    Parses CSV text into a list of rows and cells.
    Usage: {{ csv_text|parse_csv_table }}
    """
    if not csv_text:
        return []
    
    result = []
    csv_file = StringIO(csv_text)
    reader = csv.reader(csv_file)
    
    for row in reader:
        result.append([cell.strip() for cell in row])
    
    return result

@register.filter
def contains_question_placeholder(cell_text):
    """
    Checks if a cell contains a question placeholder {qX}.
    Usage: {{ cell_text|contains_question_placeholder }}
    """
    if not cell_text:
        return False
    
    pattern = r'\{\{q(\d+)\}\}'
    return re.search(pattern, cell_text) is not None

@register.filter
def extract_question_number(cell_text):
    """
    Extracts the question number from a placeholder cell {qX}.
    Usage: {{ cell_text|extract_question_number }}
    """
    if not cell_text:
        return None
    
    pattern = r'\{\{q(\d+)\}\}'
    match = re.search(pattern, cell_text)
    
    if match:
        return int(match.group(1))
    
    return None

@register.filter
def get_question_by_order(question_list, order_number):
    """
    Gets a question from a list by its order number.
    Usage: {{ question_list|get_question_by_order:order_number }}
    """
    if not question_list or not order_number:
        return None
    
    for question in question_list:
        if question.order_number == order_number:
            return question
    
    return None