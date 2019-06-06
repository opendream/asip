from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, Resolver404


def validate_reserved_url(value, resp=False):
    try:
        view, args, kwargs = resolve('/%s/' % value)
    except Resolver404:
        return True

    if view.func_name not in settings.OWNER_URL_VIEWS:
        if resp:
            return False
        else:
            raise ValidationError(_('This permalink is already in use'), params={'value': value})

    return True