from django.conf.urls import url, patterns
from common.constants import STATUS_PUBLISHED
from special.models import Page
from special.views import page_detail


permalinks = Page.objects.filter(status=STATUS_PUBLISHED).values_list('permalink', flat=True)
permalinks = set(permalinks)

permalinks |= set([p.lower() for p in permalinks])
pages = '|'.join(list(permalinks))

urlpatterns = patterns('special.views',
    url(r'^(?P<permalink>(%s)+)/$' % pages, page_detail, name='page_detail'),
)