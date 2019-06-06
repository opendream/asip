from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^updates/news/create/$', 'cms.views.news_create', name='news_create'),
    url(r'^updates/news/(?P<news_id>\d+)/edit/$', 'cms.views.news_edit', name='news_edit'),

    url(r'^updates/news/(?P<news_permalink>[A-Za-z0-9-_.]+)/(?P<news_id>\d+)/$', 'cms.views.news_detail', name='news_detail'),
    url(r'^updates/news/(?P<news_permalink>[A-Za-z0-9-_.]+)/$', 'cms.views.news_detail', name='news_detail_redirect'),
    url(r'^updates/news/$', 'cms.views.article_list', name='news_list'),

    #================ Article =================
    url(r'^article/create/$', 'cms.views.news_create', name='article_create'),
    url(r'^article/(?P<article_category>[A-Za-z0-9-_.]+)/create/$', 'cms.views.news_create', name='article_create_with_category'),
    url(r'^article/(?P<news_id>\d+)/edit/$', 'cms.views.news_edit', name='article_edit'),

    url(r'^article/(?P<article_category>[A-Za-z0-9-_.]+)/(?P<news_permalink>[A-Za-z0-9-_.]+)/(?P<news_id>\d+)/$', 'cms.views.article_detail', name='article_detail'),
    url(r'^article/news/(?P<news_permalink>[A-Za-z0-9-_.]+)/$', 'cms.views.news_detail', name='news_detail_redirect'),
    url(r'^article/(?P<article_category>[A-Za-z0-9-_.]+)/$', 'cms.views.article_list', name='article_list'),
    #============ Event =======================

    url(r'^updates/event/(?P<event_id>\d+)/edit/$', 'cms.views.event_edit', name='event_edit'),
    url(r'^updates/event/create/$', 'cms.views.event_create', name='event_create'),
    url(r'^updates/event/past/$', 'cms.views.event_past_list', name='event_past_list'),

    url(r'^updates/event/(?P<event_permalink>[A-Za-z0-9-_.]+)/(?P<event_id>\d+)/$', 'cms.views.event_detail', name='event_detail'),
    url(r'^updates/event/(?P<event_permalink>[A-Za-z0-9-_.]+)/$', 'cms.views.event_detail', name='event_detail_redirect'),
    url(r'^updates/event/$', 'cms.views.event_list', name='event_list'),

    url(r'^updates/$', 'cms.views.updates_landing', name='updates_landing'),
)