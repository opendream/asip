from django.conf.urls import url, patterns

urlpatterns = patterns('organization.views',

    url(r'^organization/(?P<organization_id>\d+)/program/create/$', 'program_create', name='program_create'),
    url(r'^organization/(?P<organization_id>\d+)/job/create/$', 'job_create', name='job_create'),
    url(r'^organization/(?P<organization_id>\d+)/in_the_news/create/$', 'in_the_news_create', name='in_the_news_create'),


    url(r'^staff/inline_invitation/$', 'staff_inline_invite', name='staff_inline_invitation'),
    url(r'^staff/(?P<staff_id>\d+)/edit/$', 'staff_edit', name='staff_edit'),

    url(r'^job/create/$', 'job_create_standalone', name='job_create_standalone'),
    url(r'^job/browse/$', 'job_list', name='job_list'),
    url(r'^job/apply/$', 'job_apply', name='job_apply'),
    url(r'^job/applying/$', 'job_applying_list', name='job_applying_list'),
    url(r'^job/applying/(?P<apply_id>\d+)/$', 'job_applying_detail', name='job_applying_detail'),

    url(r'^job/(?P<job_id>\d+)/edit/$', 'job_edit', name='job_edit'),
    url(r'^job/(?P<job_id>\d+)/$', 'job_detail', name='job_detail'),
    url(r'^job/$', 'job_landing', name='job_landing'),

    url(r'^program/create/$', 'program_create_instance', name='program_create_instance'),
    url(r'^program/inline/create/$', 'program_inline_create', name='program_inline_create'),
    url(r'^program/(?P<program_id>\d+)/edit/$', 'program_edit', name='program_edit'),

    url(r'^in_the_news/(?P<in_the_news_id>\d+)/edit/$', 'in_the_news_edit', name='in_the_news_edit'),
)