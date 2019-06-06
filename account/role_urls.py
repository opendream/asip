from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('account.views',
    url(r'^(?P<user_role_permalink>[A-Za-z0-9-_.]+)/people/$', 'people_role_list', name='people_role_list'),
)