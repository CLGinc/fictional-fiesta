from ast import literal_eval

from django import template

register = template.Library()


@register.filter(is_safe=True)
def json_to_dict(value):
    converted_value = literal_eval(value)
    if isinstance(converted_value, dict):
        return converted_value
    return value
