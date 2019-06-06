from haystack import indexes
from cms.models import News
from common.constants import STATUS_PUBLISHED
from organization.models import Organization, Job


class NewsIndex(indexes.ModelSearchIndex, indexes.Indexable):

    content_type = indexes.CharField(default='News')

    topics = indexes.MultiValueField(indexed=True, stored=True)
    categories = indexes.MultiValueField(indexed=True, stored=True)
    cms_has_party_src = indexes.MultiValueField(indexed=True, stored=True)
    tag_set = indexes.MultiValueField(indexed=True, stored=True)

    has_relation = indexes.BooleanField(indexed=True, stored=True, default=True)
    is_published = indexes.BooleanField(indexed=True, stored=True)

    class Meta:
        model = News

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter(status=STATUS_PUBLISHED)

    def prepare_is_published(self, object):
        return bool(object.status > 0)

    def prepare_categories(self, object):
        return [inst.permalink for inst in object.categories.all()]

    def prepare_topics(self, object):
        return [inst.permalink for inst in object.topics.all()]

    def prepare_cms_has_party_src(self, object):
        return [inst.dst.get_display_name() for inst in object.cms_has_party_src.all()]

    def prepare_tag_set(self, object):
        return [inst.name for inst in object.tag_set.all()]

