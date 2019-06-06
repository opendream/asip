from django.contrib import auth
from django.contrib.auth import logout
from django.utils.functional import SimpleLazyObject
from party.models import Party


def _get_logged_in_party(request):

    logged_in_party_id = request.session.get('_logged_in_party_id')
    if not logged_in_party_id:
        logged_in_party_id = request.user.id or None

    if logged_in_party_id:
        try:
            return Party.objects.get(id=logged_in_party_id)
        except Party.DoesNotExist:
            logout(request)


    return None


def get_logged_in_party(request):

    if not hasattr(request, '_cached_logged_in_party'):
        try:
            request._cached_logged_in_party = _get_logged_in_party(request)
        except AttributeError:
            request._cached_logged_in_party = None

    return request._cached_logged_in_party


class PartyMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Party authentication middleware requires authentication middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.auth.middleware.AuthenticationMiddleware' before "
            "'party.middleware.PartyMiddleware'."
        )

        request.logged_in_party = SimpleLazyObject(lambda: get_logged_in_party(request))