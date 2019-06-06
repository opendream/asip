from django import template
from organization.functions import organization_render_reference

from organization.models import Organization

register = template.Library()

@register.filter(name='organization_render_reference')
def do_organization_render_reference(organization_id, escape=False):

    organization = Organization.objects.get(id=organization_id)
    output = organization_render_reference(organization)


    if escape:
        output = output.replace("'", "\\'")

    return output