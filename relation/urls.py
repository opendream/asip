from django.conf.urls import url, patterns

urlpatterns = patterns('relation.views',
    url(r'^experience/(?P<experience_id>\d+)/edit/$', 'experience_edit', name='user_experience_organization_edit'),
    url(r'^experience/create/$', 'experience_create', name='user_experience_organization_create'),
    url(r'^received_funding/(?P<received_funding_id>\d+)/edit/$', 'received_funding_edit',
       name='party_received_funding_party_edit'),
    url(r'^received_funding/create/$', 'received_funding_create', name='party_received_funding_party_create'),

    url(r'^invite_testify/create/(?P<party_id>\d+)/$', 'invite_testify_create', name='party_invite_testify_party_create'),


)