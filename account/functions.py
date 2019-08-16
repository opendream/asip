from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from common.constants import STATUS_DRAFT
from common.functions import instance_get_thumbnail, common_clean


def user_render_reference(user, display_edit_link=False, field_name='admins'):


    html = '<span class="reference-span">%s</span>' % user.get_display_name(allow_email=False)

    if user.image:
        html = '<img class="reference-span" src="%s" /> %s' % (instance_get_thumbnail(user, field_name='image', size='50x50'), html)

    if display_edit_link:
        html = '%s <a class="reference-span autocomplete-add-another pull-right" id="edit_id_%s" href="%s?_popup=1"><span class="glyphicon glyphicon-edit"></span> %s</a>' % (html, field_name, reverse('account_edit', args=[user.id]), _('edit'))

    html = '<span class="people-reference-wrapper reference-wrapper">%s</span>' % html

    return common_clean(html)


def user_can_edit(request, instance, bypass_created=False):

    try:
        return request.user.can_edit(request, instance, bypass_created)
    except:
        return False


def user_can_edit_check(request, instance):

    if not request.user.can_edit(request, instance):
        raise PermissionDenied()


def user_can_update_status(request, instance, data=None):

    dst_field = 'dst'

    if hasattr(instance, 'REQUIRED_APPROVAL') and not instance.REQUIRED_APPROVAL:
        dst_field = 'src'


    if hasattr(instance, 'swap') and instance.swap:
        dst_field = 'src' if dst_field == 'dst' else 'dst'


    if not hasattr(instance, dst_field):
        return True

    if not data:
        data = request.GET

    num = 1
    if data.get('pk'):
        num += 1
    if data.get('dst'):
        num += 1
    if data.get('dst_id'):
        num += 1

    dst_instance = getattr(instance, dst_field)

    return request.user.is_staff or (
        len(list(data)) == num and
        (data.get('status') is not None) and
        (user_can_edit(request, dst_instance) or dst_instance.get_status() == STATUS_DRAFT)
    )
