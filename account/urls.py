from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('account.views',
    url(r'^register/$', 'account_register', name='account_register'),
    url(r'^register_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'account_register_confirm', name='account_register_confirm'),
    url(r'^login/$', 'account_login', name='account_login'),
    url(r'^logout/$', 'account_logout', {'next_page': settings.LOGIN_URL}, name='account_logout'),

    url(r'^edit/$', 'account_edit', name='account_edit'),
    url(r'^password_reset/$', 'account_reset_password', name='account_reset_password'),
    url(r'^password_reset/done/$', 'account_reset_password_done', name='account_reset_password_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            'account_reset_password_confirm', name='account_reset_password_confirm'),
    url(r'^settings/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'account_settings_confirm', name='account_settings_confirm'),

    url(r'^invitation/$', 'account_invite', name='account_invite'),
    url(r'^inline_invitation/$', 'account_inline_invite', name='account_inline_invite'),

    url(r'^app/$', 'account_app', name='account_app'),
    url(r'^app/$', 'account_app', name='account_app'),
    url(r'^app/create/$', 'account_app_form', name='account_app_create'),
    url(r'^app/(?P<pk>\d+)/$', 'account_app_detail', name='account_app_detail'),
    url(r'^app/(?P<pk>\d+)/edit/$', 'account_app_form', name='account_app_edit'),
    url(r'^connect/$', 'account_connect', name='account_connect'),
    url(r'^connect.js$', 'account_connect_js', name='account_connect_js'),
    url(r'^app/post-message/$', 'account_app_post_message', name='account_app_post_message_simple'),
    url(r'^app/post-message/(?P<token>[0-9A-Za-z_\-]+)/$', 'account_app_post_message', name='account_app_post_message'),

    #url(r'^invitation/(?P<invitation_key>\w+)/$', 'claim_user_invitation', name='claim_user_invitation'),

    # Social Auth
    url(r'^login/(?P<provider>[A-Za-z0-9-_.]+)/$', 'login_social', name='login_social'),
    url(r'^redirect/$', 'login_social_redirect', name='login_social_redirect'),
    (r'^error/', TemplateView.as_view(template_name="account/login_error.html")),

    # Detail
    url(r'^$', 'account_detail', name='account'),
)
