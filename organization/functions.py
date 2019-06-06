from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from common.constants import STATUS_PENDING
from common.functions import instance_get_thumbnail, common_clean


def organization_render_reference(organization, display_edit_link=False, field_name=''):

    html = '<span class="reference-span">%s</span>' % organization.get_display_name()

    if organization.status == STATUS_PENDING:
        html = '%s <strong class="pending">(pending)</strong>' % html

    if organization.image:
        html = '<img class="reference-span" src="%s" /> %s' % (instance_get_thumbnail(organization, field_name='image', size='50x50', crop=None), html)

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('account_edit', args=[organization.id]), _('edit'))

    html = '<span class="organization-reference-wrapper reference-wrapper title-choice">%s</span>' % html

    return common_clean(html)

def job_render_reference(job, display_edit_link=True, field_name='jobs'):

    html = '<span class="reference-span">%s</span><span class="reference-span">(%s)</span>' % (job.title, job.get_status_display())

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('job_edit', args=[job.id]), _('edit'))

    html = '<span class="job-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)

