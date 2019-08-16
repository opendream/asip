from django import template
from organization.functions import organization_render_reference, staff_render_reference

from organization.models import Organization, OrganizationStaff

register = template.Library()

@register.filter(name='organization_render_reference')
def do_organization_render_reference(organization_id, escape=False):

    organization = Organization.objects.get(id=organization_id)
    output = organization_render_reference(organization)


    if escape:
        output = output.replace("'", "\\'")

    return output


@register.filter(name='staff_render_reference')
def do_staff_render_reference(staff_id, escape=False):

    user = OrganizationStaff.objects.get(id=int(staff_id))
    output = staff_render_reference(user)

    if escape:
        output = output.replace("'", "\\'")

    return output