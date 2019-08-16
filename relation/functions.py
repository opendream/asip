from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from common.constants import STATUS_PUBLISHED, STATUS_REJECTED
from common.functions import instance_get_thumbnail, common_clean


def experience_render_reference(experience, display_edit_link=True, field_name='experiences'):

    html = '<span class="reference-span job-title">%s</span>' % experience.title
    image = instance_get_thumbnail(experience.dst, field_name='image', size='50x50', crop=None)
    if image:
        html = '%s at <img class="reference-span" src="%s" /> %s' % (html, image, experience.dst.name)
    else:
        html = '%s at %s' % (html, experience.dst.name)

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('user_experience_organization_edit', args=[experience.id]), _('edit'))

    html = '<span class="experience-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)

def received_funding_render_reference(received_funding, display_edit_link=True, field_name='received_fundings'):



    if 'receive' in field_name:

        verb_display ='Receives funding'
        if 'invest' in field_name:
            verb_display = 'Receives investing'

        html = '<span class="reference-span">%s <strong>%s</strong> from</span>' % (verb_display, received_funding.money_amount)
        target = received_funding.dst
    else:

        verb_display ='Gives funding'
        if 'invest' in field_name:
            verb_display = 'Gives investing'

        html = '<span class="reference-span">%s <strong>%s</strong> to</span>' % (verb_display, received_funding.money_amount)
        target = received_funding.src

    if target:
        image = instance_get_thumbnail(target.get_inst(), field_name='image', size='50x50')
        if image:
            html = '%s <img class="reference-span" src="%s" /> %s' % (html, image, target.get_display_name())
        else:
            html = '%s %s' % (html, target.get_display_name())

    else:
        received_funding.delete()
        return common_clean('<span class="reference-span">Deleted record</span>')


    if received_funding.status == STATUS_PUBLISHED:
        html += '<span class="required-approval approval">Approved</span>'
    elif received_funding.status == STATUS_REJECTED:
        html += '<span class="required-approval reject">Rejected</span>'


    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('party_received_funding_party_edit', args=[received_funding.id]), _('edit'))

    html = '<span class="received_funding-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)
