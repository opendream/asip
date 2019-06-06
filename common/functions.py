import random
import shutil
import bleach
import datetime
from django.conf import settings
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.urlresolvers import reverse
from django.forms import formsets
from django.template import loader, Context
from django.utils import six
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _


from django import template
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines, slugify
from django.template.loader_tags import BlockNode, ExtendsNode
import math
from sorl.thumbnail import get_thumbnail
from files_widget.controllers import ImagePath

from files_widget.forms import UnicodeWithAttr
from common.constants import STATUS_PUBLISHED, STATUS_PENDING, NO_IP

import os
import re
import urllib

register = template.Library()

def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def underscore_to_camelcase(name):
    return ''.join([c.title() for c in name.split('_')])

def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))

def process_status(user, status, default=False):

    if default:
        return STATUS_PUBLISHED if user.is_staff or settings.ALLOWED_CREATE_ORGANIZATION_WITHOUT_APPROVAL else STATUS_PENDING

    status = int(status)
    if not user.is_staff and status == STATUS_PUBLISHED:
        status = STATUS_PENDING

    return status

def get_success_message(inst=False, is_new=False, args=[]):

    if not inst:
        return _('Complete created')


    inst_name = inst.get_inst_type_human_readable().lower()

    if hasattr(inst, 'permalink'):
        args.append(inst.permalink)
    elif hasattr(inst, 'username'):
        args.append(inst.username)

    args.append(inst.id)

    if is_new:
        # return  _('New %s have been created. View this %s <a href="%s">here</a>.') % (
        return  _('New %s have been created.') % (
            _(inst_name),
            # _(inst_name),
            # reverse('%s_detail' % inst_type, args=args)
        )
    else:
        # return _('Your %s settings have been updated. View this %s <a href="%s">here</a>.') % (
        return _('Your %s settings have been updated.') % (
            _(inst_name),
            # _(inst_name),
            # reverse('%s_detail' % inst_type, args=args)
        )


# Todo sum function
def get_cms_success_message(inst=False, is_new=False, args=[]):
    if not inst:
        return _('Complete created')


    inst_name = inst.inst_name.lower()
    if hasattr(inst, 'permalink'):
        args.append(inst.permalink)
    elif hasattr(inst, 'username'):
        args.append(inst.username)

    args.append(inst.id)

    if is_new:
        return  _('New article has been created. View this article <a href="%s">here</a>.') % (
            inst.get_absolute_url()
        )
    else:
        return _('Your article settings has been updated. View this article <a href="%s">here</a>.') % (
           inst.get_absolute_url()
        )

# Render specific blocks from templates

def get_template(template):
    if isinstance(template, (tuple, list)):
        return loader.select_template(template)
    return loader.get_template(template)


class BlockNotFound(Exception):
    pass


def render_template_block(template, block, context):
    """
    Renders a single block from a template. This template should have previously been rendered.
    """
    return render_template_block_nodelist(template.nodelist, block, context)


def render_template_block_nodelist(nodelist, block, context):
    for node in nodelist:
        if isinstance(node, BlockNode) and node.name == block:
            return node.render(context)
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            if hasattr(node, key):
                try:
                    return render_template_block_nodelist(getattr(node, key), block, context)
                except:
                    pass
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                return render_template_block(node.get_parent(context), block, context)
            except BlockNotFound:
                pass
    raise BlockNotFound


def render_block_to_string(template_name, block, dictionary=None, context_instance=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.
    """
    dictionary = dictionary or {}
    t = get_template(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    t.render(context_instance)
    return render_template_block(t, block, context_instance)


def instance_save_image_from_url(instance, image_url, field_name='image', append=False, rand=False):
    # Use save_form_data like model form
    image_field = instance._meta.get_field(field_name)
    if image_field:
        # determined temp path of file widget
        file_name = image_url.split('?')[0]
        file_name_list = file_name.split('/')

        # find the name of file
        while len(file_name_list):
            file_name = file_name_list.pop()
            if file_name:
                if not re.search('_(\d+)\.(jpg|jpef|png|gif)$', file_name, re.IGNORECASE):
                    file_name = '%s.jpg' % file_name
                break

        image_temp_dir = '%s%s' % (settings.FILES_WIDGET_TEMP_DIR, instance.id)
        image_temp_path = '%s/%s' % (image_temp_dir, file_name)

        # prepare directory
        media_image_temp_dir = '%s/%s' % (settings.MEDIA_ROOT, image_temp_dir)
        if not os.path.isdir(media_image_temp_dir):
            os.makedirs(media_image_temp_dir)

        # download origin image to temp path
        if rand:
            image_url = '%s?a=%s' % (image_url, random.randint(1, 100000000000))

        urllib.urlretrieve(image_url, '%s/%s' % (settings.MEDIA_ROOT, image_temp_path))

        # move file from temp to upload automatically
        if not append:
            setattr(instance, field_name, '')

        image_field.save_form_data(instance, UnicodeWithAttr('%s' % image_temp_path))
        instance.save()

    else:
        raise AttributeError


def instance_get_thumbnail(instance=None, field_name='image', size='430x320', crop='center', upscale=True, bypass_image=None, no_default=False):
    # prepare default image in case initial
    full_dir = os.path.join(settings.MEDIA_ROOT, 'default_images')

    if not os.path.exists(full_dir):
        shutil.copytree('.%s' % os.path.join(settings.STATIC_URL, 'images/default'), full_dir)

    if bypass_image:
        image = bypass_image
    else:
        image = getattr(instance, field_name)

    if image:

        if hasattr(image, 'all'):

            image_list = []

            for item in image.all():
                item = instance_get_thumbnail(instance, field_name, size, crop, upscale, item, no_default=no_default)
                image_list.append(item)

            return image_list

        try:
            file_extension = image.filename.split('.')[-1].lower()
        except:
            file_extension = 'png'

        format = 'PNG'

        if file_extension == 'jpg' or file_extension == 'jpeg':
            format = 'JPEG'
        elif file_extension == 'png':
            format = 'PNG'
        elif file_extension == 'gif':
            format = 'GIF'


        from sorl.thumbnail import base
        base.EXTENSIONS.update({'GIF': 'gif'})

        try:
            return get_thumbnail(image, size, crop=crop, upscale=upscale, format=format).url
        except IOError:
            try:
                return get_thumbnail(image, size, crop=crop, upscale=upscale, format='JPEG').url
            except IOError:
                print 'Error unknow image format'

    if no_default:
        return None

    # default image by gender
    if hasattr(instance, 'gender'):
        if instance.gender:
            image = ImagePath('%s/default-%s.jpg' % (full_dir, instance.gender.lower()))
            try:
                return get_thumbnail(image, size, crop=crop, upscale=upscale).url
            except:
                return False

    image = ImagePath('%s/default-o.jpg' % full_dir)

    # Garantie just return an image
    return get_thumbnail(image, size, crop=crop, upscale=upscale).url


def staff_required(request):
    defaults = {
        'template_name': 'admin/login.html',
        'authentication_form': AdminAuthenticationForm,
        'extra_context': {
            'title': _('Log in'),
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        },
    }
    return login(request, **defaults)

def instance_set_permalink(instance, title, field_name='permalink'):
    ModelClass = instance.__class__

    origin_permalink = slugify(title)

    if len(origin_permalink) <= 3:
        origin_permalink = 'pending'

    permalink = origin_permalink

    latest = type(instance).objects.filter(**{'%s__startswith' % field_name: '%s-' % origin_permalink}).order_by(field_name)

    increment_number = 1

    if latest.count() == 0:
        increment_number = 1
    else:

        latest = latest[0]
        try:
            increment_number = int(getattr(latest, field_name).split('-')[-1])
        except ValueError:
            increment_number = 1

    while True:
        try:
            ModelClass.objects.get(**{field_name: permalink})
        except ModelClass.DoesNotExist:
            setattr(instance, field_name, permalink)
            break

        permalink = "%s-%s" % (origin_permalink, increment_number)
        increment_number = increment_number + 1


def generate_year_range(prev_years=30, choices=False, required=False, empty_label='Year', next_years=None):
    this_year = datetime.date.today().year
    if next_years:
        this_year += next_years
    years = range(this_year - prev_years, this_year)
    years.reverse()

    if choices:
        years = zip(years, years)

        if not required:
            years.insert(0, (None, empty_label))

    return years


def common_clean(value):
    ALLOWED_TAGS = [
        'p', 'em', 'strong', 'span', 'a', 'br', 'strong', 'ul', 'ol', 'li', 'img',
        'h3', 'h4', 'h5', 'h6',
        'table', 'thead', 'tbody', 'tfoot', 'th', 'tr', 'td', 'caption',
        's', 'u', 'iframe', 'embed', 'object'
    ]
    ALLOWED_ATTRIBUTES = {
        '*': ['class'],
        'a': ['href', 'rel', 'id', 'target', 'class'],
        'img': ['src', 'alt', 'ta-insert-video', 'allowfullscreen', 'frameborder', 'style', 'class', 'width', 'height'],
        'iframe': ['src', 'allowfullscreen', 'frameborder', 'width', 'height'],
        'table': ['align', 'bgcolor', 'border', 'cellpadding', 'cellspacing', 'frame', 'rules', 'sortable', 'summary', 'width']
    }

    return bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)


def get_point(form_list, POINT, keys, update=False):

    point_map = []

    for key in keys:
        point_map.extend(POINT[key].items())
    point_map = dict(point_map)

    max_total = 0
    total = 0
    for field_name, point in point_map.iteritems():
        max_total += point

        value = None
        for form in form_list:

            try:
                if update:
                    value = form.cleaned_data[field_name]
                else:
                    value = form.initial[field_name]
            except KeyError:
                pass

        if value:
            total += point

    if max_total == 0:
        return 0


    return min(100, int(math.ceil(float(total)/float(max_total)*100)))

def get_ip_address(request):

    ip_address = NO_IP

    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    except:
        pass

    return ip_address

class PermanentTokenGenerator(PasswordResetTokenGenerator):
    def _make_token_with_timestamp(self, user, timestamp):

        ts_b36 = int_to_base36(timestamp)
        key_salt = "django.contrib.auth.tokens.PermanentTokenGenerator"

        # Ensure results are consistent across DB backends
        login_timestamp = user.last_login.replace(microsecond=0, tzinfo=None)

        value = (six.text_type(user.pk) + user.password +
                 six.text_type(timestamp))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)






def rget(data, key, default=None):

    value = data
    for k in key.split('.'):
        try:
            value = value[k]
        except KeyError:
            return default

    return value
