from django.conf.urls import url, patterns
from organization.views import organization_detail

urlpatterns = patterns('organization.views',

    url(r'^(?P<organization_role_permalink>[A-Za-z0-9-_.]+)/organization/$', 'organization_role_list', name='organization_role_list'),

    #url(r'^(?P<organization_role_permalink>[A-Za-z0-9-_.]+)/(?P<organization_permalink>[A-Za-z0-9-_.]+)/$', 'organization_role_detail', name='organization_role_detail'),
    url(r'^(?P<organization_permalink>[A-Za-z0-9-_.]+)/$', organization_detail, name='organization_detail'),

    url(r'^(?P<organization_role_permalink>[A-Za-z0-9-_.]+)/(?P<organization_type_permalink>[A-Za-z0-9-_.]+)/organization/$',
        'organization_role_list', name='organization_role_type_list'),

)