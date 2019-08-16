import os
import autocomplete_light
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.conf.urls.i18n import i18n_patterns

autocomplete_light.autodiscover()
admin.autodiscover()

CUSTOM_ENABLED = True
try:
    import custom.urls
except ImportError:
    CUSTOM_ENABLED = False


# urlpatterns = i18n_patterns('', # not trans now
urlpatterns = patterns('',
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^files-widget/', include('files_widget.urls')),
    url(r'^account/', include('account.urls', app_name='accoount')),
    url(r'^people/', include('account.people_urls', app_name='account')),
    url(r'^organization/', include('organization.urls', app_name='organization')),
    url(r'^people/', include('account.people_urls', app_name='account')),
    url(r'^forum/', include('forum.urls', app_name='forum')),

    url(r'^api/', include('api.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'', include('notification.urls')),
    url(r'', include('taxonomy.urls', app_name='taxonomy')),

    url(r'', include('organization.job_urls', app_name='organization')),
    url(r'', include('party.urls', app_name='party')),
    url(r'', include('relation.urls', app_name='relation')),
    url(r'', include('cms.urls', app_name='cms')),
    url(r'', include('account.connect_urls', app_name='account')),

    url(r'', include('social_auth.urls')),
    url(r'', include('presentation.urls', app_name='presentation')),
    # No swap order url
    url(r'', include('account.role_urls', app_name='account')),
    url(r'', include('special.urls', app_name='special')),
    url(r'', include('organization.role_urls', app_name='organization')),

)

if CUSTOM_ENABLED:
    # urlpatterns += i18n_patterns('', # not trans now
    urlpatterns += patterns('',

        url(r'', include('custom.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
        url(r'^404$', TemplateView.as_view(template_name='404.html')),
        url(r'^500$', TemplateView.as_view(template_name='500.html')),
    )

    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

else:
    urlpatterns += patterns('',
        url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    )


handler403 = 'presentation.views.handler403'