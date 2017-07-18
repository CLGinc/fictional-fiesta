from urllib.parse import urljoin

from django import template

register = template.Library()


@register.filter(is_safe=True)
def resize(value, arg):
    if 'google' in value:
        return urljoin(value, '?sz={0}'.format(arg))
    elif 'facebook' in value:
        return urljoin(value, '?height={0}&width={0}'.format(arg))
    return value
