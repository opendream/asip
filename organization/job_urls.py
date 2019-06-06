from django.conf.urls import url, patterns

urlpatterns = patterns('organization.views',

    url(r'^organization/(?P<organization_id>\d+)/job/create/$', 'job_create', name='job_create'),
    url(r'^job/create/$', 'job_create_standalone', name='job_create_standalone'),
    url(r'^job/(?P<job_id>\d+)/edit/$', 'job_edit', name='job_edit'),
    url(r'^job/(?P<job_id>\d+)/$', 'job_detail', name='job_detail'),
    url(r'^job/$', 'job_list', name='job_list'),

)