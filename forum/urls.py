from django.conf.urls import url, patterns

urlpatterns = patterns('forum.views',

    # Form
    url(r'^create/$', 'forum_form', name='forum_create'),
    url(r'^(?P<pk>\d+)/edit/$', 'forum_form', name='forum_edit'),

    url(r'^(?P<parent_pk>\d+)/board/create/$', 'forum_board_form', name='forum_board_create'),
    url(r'^board/(?P<pk>\d+)/edit/$', 'forum_board_form', name='forum_board_edit'),

    url(r'^board/(?P<parent_pk>\d+)/topic/create/$', 'forum_topic_form', name='forum_topic_create'),
    url(r'^topic/(?P<pk>\d+)/edit/$', 'forum_topic_form', name='forum_topic_edit'),

    url(r'^topic/(?P<parent_pk>\d+)/post/create/$', 'forum_post_form', name='forum_post_create'),
    url(r'^post/(?P<pk>\d+)/edit/$', 'forum_post_form', name='forum_post_edit'),

    url(r'^post/(?P<parent_pk>\d+)/reply/create/$', 'forum_reply_form', name='forum_reply_create'),
    url(r'^reply/(?P<pk>\d+)/edit/$', 'forum_reply_form', name='forum_reply_edit'),

    # Detail
    url(r'^(?P<permalink>[\w._-]+)/$', 'forum_detail', name='forum_detail'),
    url(r'^board/(?P<permalink>[\w._-]+)/$', 'forum_board_detail', name='forum_board_detail'),
    url(r'^topic/(?P<permalink>[\w._-]+)/$', 'forum_topic_detail', name='forum_topic_detail'),
    url(r'^post/(?P<pk>\d+)/$', 'forum_post_detail', name='forum_post_detail'),
    url(r'^reply/(?P<pk>\d+)/$', 'forum_reply_detail', name='forum_reply_detail'),

)