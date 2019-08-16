from django import template
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import six
from haystack.query import SearchQuerySet
from common.functions import get_point

register = template.Library()

@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output  
        return ''


@register.simple_tag(name='render_formset')
def render_formset(field_formset, field_formset_id, field_formset_title, fixed=False):

    for field_form in field_formset:

        show_delete = False

        for field in field_form:
            if field.value():
                show_delete = True
                break

        if not show_delete:
            field_form['DELETE'].field.widget.attrs['class'] = 'hidden'


    return render_to_string('formset.html', {
        'field_formset': field_formset,
        'field_formset_id': field_formset_id,
        'field_formset_title': field_formset_title,
        'fixed': fixed
    })


@register.filter()
def to_int(value):
    return int(value)

@register.filter(name='formset_error_valid')
def formset_error_valid(value):

    valid_error = False
    for value_error in value:
        if value_error:
           valid_error = True

    if not valid_error:
        return False
    else:
        return value


@register.filter()
def filter_status(queryset, status):
    return queryset.filter(status=status)

@register.filter()
def order_status(queryset):
    return queryset.order_by('-status', '-changed')

@register.filter()
def keyvalue(dict, key):
    return dict[key]

@register.filter
def filter(queryset, fv):
    f, v = fv.split('=')

    if f == 'party_roles__permalink':
        return queryset.filter(Q(organization__organization_roles__permalink=v) | Q(user__user_roles__permalink=v))
    elif f == 'party_status':
        return queryset.filter(Q(organization__status=v) | Q(user__is_active=bool(int(v))))

    return queryset.filter(**{f: v})

@register.filter
def exclude(queryset, fv):
    f, v = fv.split('=')
    return queryset.exclude(**{f: v})

@register.filter
def count(queryset):
    return queryset.count()

@register.filter
def filter_key(items, key):
    return [item for item in items if item.get(key)]

@register.filter
def exclude_key(items, key):
    return [item for item in items if not item.get(key)]

@register.simple_tag(name='get_point')
def get_point_tag(form_list, keys):
    keys = keys or []
    return get_point(form_list, settings.POINT, keys)

def render_form_field_errors(form):
    return render_to_string('common/form-field-errors.html', {'form': form})

@register.filter
def get_search_text(instance):
    try:
        obj = SearchQuerySet().models(type(instance)).filter(django_id=instance.id)[0]
        return obj.text
    except IndexError:
        instance.save()

    return ''

@register.filter
def times(number):
    return range(number)

@register.filter
def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

@register.simple_tag(takes_context=True)
def vary_print(context, field):
    if context.get('vary_print', False):
        return '<div class="virtual-textarea">%s</div>' % field.value()
    return field

@register.filter(name='any')
def do_any(value):
    return any(value)

@register.filter(name='all')
def do_all(value):
    return all(value)

@register.filter(name='do_and')
def do_and(value1, value2):
    return bool(value1 and value2)

@register.filter(name='do_or')
def do_or(value1, value2):
    if type(value2) == list and len(value2) == 2 and value2[0] == '' and value2[1] == 'THB':
        value2 = False
    return bool(value1 or value2)

@register.filter(name='do_or_false')
def do_or_false(value1, value2):
    return bool(value1 or (value2 is not None and value2 != ''))

@register.filter(name='split')
def do_split(value1, value2):
    return value1.split(value2)