from django.conf.urls import url, patterns

urlpatterns = patterns('organization.views',
    url(r'^(?P<organization_id>\d+)/edit/$', 'organization_edit', name='organization_edit'),
    url(r'^(?P<organization_id>\d+)/generate-pdf/(?P<bypass_key>[A-Za-z0-9-_.]+)/$', 'organization_generate_pdf', name='organization_generate_pdf'),
    url(r'^(?P<organization_id>\d+)/pdf/$', 'organization_pdf', name='organization_pdf'),

    url(r'inline/create/$', 'organization_inline_create', name='organization_inline_create'), # TODO: fixed
    url(r'^(?P<type_of_organization>[A-Za-z0-9-_.]+)/create/$', 'organization_create', name='organization_create'),
    #url(r'^(?P<organization_permalink>[A-Za-z0-9-_.]+)/$', 'organization_detail', name='organization_detail'),
    url(r'^(?P<type_of_organization>[A-Za-z0-9-_.]+)/$', 'organization_type_list', name='organization_type_list'),
    url(r'^$', 'organization_list', name='organization_list'),

)