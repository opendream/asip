from django.conf.urls import patterns, url

urlpatterns = patterns('taxonomy.views',
    url(r'^organization-type/(?P<permalink>[A-Za-z0-9-_.]+)/$', 'organization_type_detail', name='organization_type_detail'),
)