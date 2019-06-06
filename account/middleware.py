from django.core.urlresolvers import reverse
from social_auth.exceptions import AuthCanceled
from social_auth.middleware import SocialAuthExceptionMiddleware

class AccountSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):

    def get_message(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return ''
        else:
            return unicode(exception)

    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return reverse('home')
        else:
            return super(AccountSocialAuthExceptionMiddleware, self).get_redirect_uri(request, exception)