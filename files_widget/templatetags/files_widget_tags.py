import re
import urllib

from django import template


register = template.Library()

@register.filter
def thumbnail_format(path):
    match = re.search(r'\.\w+$', path)
    if match:
        ext = match.group(0)
        if ext.lower() in ['.gif', '.png']:
            return 'PNG'
    return 'JPEG'

@register.filter
def filename_from_path(path):
    return re.sub(r'^.+\/', '', path)

@register.filter
def unquote(value):
    "urldecode"
    return urllib.unquote(value)

@register.filter
def is_image(path):
    try:
        file_type = path.split('.')[-1].lower()
        return file_type in ['png', 'jpeg', 'jpg', 'gif', 'tiff']
    except IndexError:
        pass

    return False


@register.filter
def first_char(path):
    try:
        file_name = path.split('/')[-1].lower()
        return file_name.decode('utf-8')[0]
    except IndexError:
        pass

    return u'-'