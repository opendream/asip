from django import template
from relation.views import invite_testify_create


register = template.Library()

@register.simple_tag(name='invite_testify_create_form', takes_context=True)
def invite_testify_create_form(context):
    request = context['request']
    party_id = context.get('party_id') or context.get('organization_id') or context.get('user_id')
    return invite_testify_create(request, party_id)
