from django.conf.urls import url, patterns

urlpatterns = patterns('party.views',
                       url(r'^portfolio/(?P<portfolio_id>\d+)/edit/$', 'portfolio_edit', name='portfolio_edit'),
                       url(r'^portfolio/create/$', 'portfolio_create', name='portfolio_create'),
                       url(r'^portfolio/(?P<portfolio_id>\d+)/$', 'portfolio_detail', name='portfolio_detail'),
                       url(r'^party/(?P<party_id>\d+)/activate/$', 'party_activate', name='party_activate'),
                       url(r'^party/deactivate/$', 'party_deactivate', name='party_deactivate'),

)