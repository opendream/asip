from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('account.views',

    url(r'^\[your-receive-new-token-path\]/$', 'account_your_receive_new_token_path', name='account_your_receive_new_token_path'),
    url(r'^complete/(?P<backend>[^/]+)/$', 'social_complete', name='socialauth_complete'),
)