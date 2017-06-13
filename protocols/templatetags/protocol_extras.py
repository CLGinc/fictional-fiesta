import json

from django import template

register = template.Library()


@register.filter(is_safe=True)
def json_to_dict(value):
    try:
        converted_value = json.loads(value)
        if isinstance(converted_value, dict):
            return converted_value
    except ValueError:
        return value
    return value
