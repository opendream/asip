from django.conf.urls import url, patterns

urlpatterns = patterns('notification.views',
    url(r'^notification/$', 'notification_list', name='notification_list'),
    url(r'^request/$', 'request_list', name='request_list'),

)