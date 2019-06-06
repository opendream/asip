import os
import urllib
import re
from django.conf import settings

from django.core.files import File
from social_auth.backends.contrib.linkedin import LinkedinBackend
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.pipeline.user import _ignore_field
from social_auth.db.django_models import UserSocialAuth

from account.models import User
from asip.settings import BASE_DIR, MEDIA_ROOT, RESERVED_USERNAMES
from common.functions import instance_save_image_from_url, rget
from taxonomy.models import Country


def rewrite_username(username):

    _username_ = username.lower().split('@')[0].replace(' ', '.')
    username = _username_
    usernames = [u for u in User.objects.values_list('username', flat=True)]
    usernames = usernames + RESERVED_USERNAMES
    increment_number = 1
    while True:
        if username in usernames:
            username = "%s%s" % (_username_, increment_number)
            increment_number += 1
        else:
            break

    return username


def generate_username(details, user=None, user_exists=UserSocialAuth.simple_user_exists, *args, **kwargs):

    if user:
        return {'username': user.username}

    username = rewrite_username(details['username'])

    validator = re.compile('^[\w.@+-]+$')

    result = {}
    if not validator.match(username):
        username = rewrite_username(details['email'])

    if not details.get('email'):
        result['email'] = 'unknow.%s@%s.com' % (kwargs['uid'], kwargs['backend'].name)
        details['email'] = result['email']

    result['username'] = rewrite_username(details['email'])

    return result


def update_profile(backend, details, response, user=None, is_new=False, *args, **kwargs):

    if not user.image:

        if isinstance(backend, LinkedinBackend):
            image_url = details.get('image')
        elif isinstance(backend, FacebookBackend):
            image_url = "https://graph.facebook.com/%s/picture?type=large" % response['id']

        if image_url:
            instance_save_image_from_url(user, image_url)


def map_extra_data(backend, details, response):

    extra_data = None


    if isinstance(backend, LinkedinBackend):
        extra_data = settings.LINKEDIN_EXTRA_DATA
    elif isinstance(backend, FacebookBackend):
        extra_data = settings.FACEBOOK_EXTRA_DATA

    if not extra_data:
        return

    for key, value in extra_data:
        details[value] = rget(response, key)

    if details.get('gender'):
        details['gender'] = details['gender'][0].upper()

    if details.get('country'):
        try:
            #details['country'] = Country.objects.get(title__iexact=details.get('country'))
            details['country'] = Country.objects.extra(
                where=["UPPER(%s) SIMILAR TO UPPER(CONCAT('%%', title_en, '%%'))"],
                params=(
                    details.get('country'),
                ),
            ).latest('id')
        except Country.DoesNotExist:
            pass

    if details.get('experiences'):
        # TODO: maybe auto create experience
        pass


def update_user_details(backend, details, response, user=None, is_new=False, *args, **kwargs):

    if user is None:
        return

    is_deleted = user.is_deleted

    if is_deleted:
        user.is_deleted = False

    changed = False  # flag to track changes

    map_extra_data(backend, details, response)


    for name, value in details.iteritems():
        # do not update username, it was already generated, do not update
        # configured fields if user already existed
        if not _ignore_field(name, is_new):
            if value and hasattr(user, name) and value != getattr(user, name, None):

                setattr(user, name, value)
                changed = True

    if changed or is_deleted:
        user.save()
