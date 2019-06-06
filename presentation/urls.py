from django.conf import settings
from django.conf.urls import url, patterns
from django.views.generic import RedirectView, TemplateView
from taxonomy.models import OrganizationRole

roles = '|'.join(OrganizationRole.objects.all().values_list('permalink', flat=True)) + '|people'

urlpatterns = patterns('presentation.views',
    url(r'^$', 'home', name='home'),
    url(r'^home/$', 'home', name='home_force', kwargs={'force': True}),
    url(r'^about/$', 'about', name='about'),
    url(r'^term/$', 'term', name='term'),
    url(r'^privacy/$', 'privacy', name='privacy'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^search/$', 'search', name='search'),
    url(r'^message/$', 'message_list', name='message_list'),

    url(r'^403/$', TemplateView.as_view(template_name="403.html")),
    url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^500/$', TemplateView.as_view(template_name="500.html")),

    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.SITE_FAVICON_URL, permanent=True)),
    url(r'^apple-touch-icon\.png$', RedirectView.as_view(url=settings.SITE_FAVICON_URL, permanent=True)),
    url(r'^apple-touch-icon-120x120\.png$', RedirectView.as_view(url=settings.SITE_FAVICON_URL, permanent=True)),
    url(r'^delete/(?P<app_label>[A-Za-z0-9-_.]+)/(?P<model_name>[A-Za-z0-9-_.]+)/(?P<id>\d+)/$', 'presentation_delete', name='presentation_delete'),

    # Staff
    url(r'^manage/$', 'manage', name='manage'),
    url(r'^manage/pending-organization/(?P<organization_role>[A-Za-z0-9-_.]+)/$', 'manage_pending_organization', name='manage_pending_organization'),
    url(r'^manage/promote-organization/(?P<organization_role>[A-Za-z0-9-_.]+)/$', 'manage_promote_organization', name='manage_promote_organization'),

    #url(r'^manage/organization/(?P<type_of_organization>[A-Za-z0-9-_.]+)/$', 'manage_porganization', name='manage_organization'),
    url(r'^manage/promote-people/$', 'manage_promote_people', name='manage_promote_people'),
    #url(r'^manage/people/$', 'manage_people', name='manage_people'),

    url(r'^(?P<role_permalink>(%s)+)/browse/$' % roles, 'presentation_role_list_browse', name='presentation_role_list_browse'),
    url(r'^(?P<role_permalink>(%s)+)/happening/$' % roles, 'presentation_role_list_happening', name='presentation_role_list_happening'),
    url(r'^(?P<role_permalink>(%s)+)/$' % roles, 'presentation_role_list_redirect', name='presentation_role_list_redirect'),
)
