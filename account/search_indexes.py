import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from haystack import indexes
from common.constants import STATUS_PUBLISHED
from relation.models import BaseRelation


class UserIndex(indexes.ModelSearchIndex, indexes.Indexable):

    content_type = indexes.CharField(default='User')
    user_roles = indexes.MultiValueField(indexed=True, stored=True)
    interests = indexes.MultiValueField(indexed=True, stored=True)
    country = indexes.CharField(indexed=True, stored=True)
    has_relation = indexes.BooleanField(indexed=True, stored=True, default=False)

    is_published = indexes.BooleanField(indexed=True, stored=True)

    job_roles =  indexes.MultiValueField(indexed=True, stored=True)
    job_locations = indexes.MultiValueField(indexed=True, stored=True)

    class Meta:
        model = get_user_model()
        fields_to_skip = ['_total_follower', '_total_following', '_total_love', '_total_testify', 'password']
        excludes = ['password']

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter()

    def prepare_user_roles(self, object):
        return [inst.permalink for inst in object.user_roles.all()]

    def prepare_interests(self, object):
        return [inst.permalink for inst in object.interests.all()]

    def prepare_job_roles(self, object):
        return [inst.permalink for inst in object.job_roles.all()]

    def prepare_job_locations(self, object):
        return [inst.permalink for inst in object.job_locations.all()]

    def prepare_country(self, object):

        if object.country:
            return object.country.permalink
        else:
            return ''

    def prepare_has_relation(self, object):
        for Model in BaseRelation.__subclasses__():
            if Model.objects.filter(Q(dst_id=object.id) | Q(src_id=object.id)).count():
                return True

        return False

    def prepare_is_published(self, object):
        # is_published = indexes.BooleanField(indexed=True, stored=True)
        return bool(object.is_active)