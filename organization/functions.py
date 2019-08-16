from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from common.constants import STATUS_PENDING, STATUS_DRAFT, STATUS_PUBLISHED, STATUS_REJECTED
from common.functions import instance_get_thumbnail, common_clean


def organization_render_reference(organization, display_edit_link=False, field_name='', instance=None, src_field_name='', dst_field_name=''):

    html = '<span class="reference-span">%s</span>' % organization.get_display_name()

    if organization.status == STATUS_PENDING:
        html = '%s <strong class="pending">(pending)</strong>' % html
    elif organization.status == STATUS_DRAFT:
        html = '%s <strong class="pending">(mock up)</strong>' % html
    elif organization.status == STATUS_PUBLISHED:
        html = '%s <strong class="pending">(approved)</strong>' % html

    if organization.image:
        html = '<img class="reference-span" src="%s" /> %s' % (instance_get_thumbnail(organization, field_name='image', size='50x50', crop=None), html)

    status_src = None
    try:
        if src_field_name and hasattr(organization, src_field_name):
            status_src = getattr(organization, dst_field_name).filter(src=instance).latest('id').status
    except:
        pass

    status_dst = None
    try:
        if dst_field_name and hasattr(organization, dst_field_name):
            status_dst = getattr(organization, src_field_name).filter(dst=instance).latest('id').status
    except:
        pass

    if (status_src is not None and status_src == STATUS_PUBLISHED) or (status_dst is not None and status_dst == STATUS_PUBLISHED):
        html += '<span class="required-approval approval">Approved</span>'
    elif (status_src is not None and status_src == STATUS_REJECTED) or (status_dst is not None and status_dst == STATUS_REJECTED):
        html += '<span class="required-approval reject">Rejected</span>'

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

def in_the_news_render_reference(in_the_news, display_edit_link=True, field_name='in_the_news'):

    html = '<span class="reference-span">%s</span>' % (in_the_news.title or in_the_news.url, )

    if in_the_news.image:
        html = '%s <img class="reference-span" src="%s" />' % (html, instance_get_thumbnail(in_the_news, field_name='image', size='50x50'))

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('in_the_news_edit', args=[in_the_news.id]), _('edit'))

    html = '<span class="in_the_news-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)

def program_render_reference(program, display_edit_link=True, field_name='programs'):

    html = '<span class="reference-span">%s</span>' % (program.name)
    if program.status == STATUS_PENDING:
        html = '%s <strong class="pending">(pending)</strong>' % html
    elif program.status == STATUS_DRAFT:
        html = '%s <strong class="pending">(mock up)</strong>' % html
    elif program.status == STATUS_PUBLISHED:
        html = '%s <strong class="pending">(approved)</strong>' % html

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (
            html, field_name, reverse('program_edit', args=[program.id]), _('edit'))

    html = '<span class="program-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)


def user_render_reference(user, display_edit_link=False, field_name='admins'):

    html = '<span class="reference-span">%s</span>' % user.get_display_name(allow_email=False)
    html = '%s<span class="name-span hidden">%s</span>' % (html, ('%s %s' % (user.first_name, user.last_name)) if user.first_name else user.get_display_name(allow_email=False))
    html = '%s<span class="email-span hidden">%s</span>' % (html, user.email)

    if user.image:
        html = '<img class="reference-span" src="%s" /> %s' % (instance_get_thumbnail(user, field_name='image', size='50x50'), html)

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (html, field_name, reverse('account_edit', args=[user.id]), _('edit'))

    html = '<span class="people-reference-wrapper reference-wrapper">%s</span>' % html
    return common_clean(html)


def staff_render_reference(staff, display_edit_link=False, field_name='admins'):
    html = '<span>' \
                '<span class=ref-wrapper>' \
                   '<span class="ref-label">Name: </span>' \
                   '<span class="ref-value">%s</span>' \
               '</span>' \
                '<span class=ref-wrapper>' \
                    '<span class="ref-label">Title</span>' \
                    '<span class="ref-value">%s</span>' \
               '</span>' \
                '<span class=ref-wrapper>' \
                    '<span class="ref-label">Email</span>' \
                    '<span class="ref-value">%s</span>' \
               '</span>' \
                '<span class=ref-wrapper>' \
                    '<span class="ref-label">Contact Number</span>' \
                    '<span class="ref-value">%s</span>' \
               '</span>' \
           '</span>' % (
        ('%s %s' % (staff.user.first_name, staff.user.last_name)) if staff.user.first_name else staff.user.get_display_name(allow_email=False),
        staff.job_title or '-',
        staff.user.email,
        staff.contact_number or '-',
    )

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (html, field_name, reverse('staff_edit', args=[staff.id]), _('edit'))

    html = '<span class="people-reference-wrapper reference-wrapper">%s</span>' % html
    return common_clean(html)



