from urlparse import urlparse
from django.conf import settings
from django.http import HttpResponse
from common.signals import request_accessor

class RequestProviderError(Exception):
    pass

class RequestProvider(object):

    def __init__(self):
        self._request = None
        request_accessor.connect(self)

    def process_request(self, request):
        self._request = request
        return None

    def __call__(self, **kwargs):
        return self._request

# ===================================================

BotNames=['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','"Baiduspider','googlebot','Speedy Spider','DotBot']

class CrawlerChecker:
    def process_request(self, request):
        user_agent=request.META.get('HTTP_USER_AGENT', None)

        if not user_agent:
            return

        request.is_crawler = False

        for botname in BotNames:
            if botname in user_agent:
                request.is_crawler = True


class ProtectApiScraper(object):
    def process_request(self, request):


        if not settings.DEBUG and request.path[1:].split('/')[0] == 'api':
            referer = request.META.get('HTTP_REFERER', '')
            referer_domain = urlparse(referer).hostname
            site_domain = request.META.get('HTTP_HOST', '').split(':')[0]

            if referer_domain != site_domain:
                return HttpResponse('Not allow crawler api', status=500)
        return None