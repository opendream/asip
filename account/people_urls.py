from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('account.views',
    url(r'^$', 'people_list', name='people_list'),
    url(r'^(?P<username>(?!browse)[\w.@+-]+)/(?P<people_id>\d+)/$', 'people_detail', name='people_detail'),
    url(r'^(?P<username>(?!browse|happening)[\w.@+-]+)/$', 'people_detail'),
    url(r'^(?P<people_id>\d+)/edit/$', 'account_edit', name='people_edit'),

)
