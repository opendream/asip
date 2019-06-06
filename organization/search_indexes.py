import datetime
from haystack import indexes
from common.constants import STATUS_PUBLISHED
from organization.models import Organization, Job


class OrganizationIndex(indexes.ModelSearchIndex, indexes.Indexable):

    content_type = indexes.CharField(default='Organization')

    type_of_needs = indexes.MultiValueField(indexed=True, stored=True)
    type_of_supports = indexes.MultiValueField(indexed=True, stored=True)
    topics = indexes.MultiValueField(indexed=True, stored=True)
    organization_roles = indexes.MultiValueField(indexed=True, stored=True)
    country = indexes.CharField(indexed=True, stored=True)
    organization_primary_role = indexes.CharField(indexed=True, stored=True)

    organization_types = indexes.MultiValueField(indexed=True, stored=True)
    investor_types = indexes.MultiValueField(indexed=True, stored=True)
    product_launch = indexes.CharField(indexed=True, stored=True)
    funding = indexes.CharField(indexed=True, stored=True)
    request_funding = indexes.CharField(indexed=True, stored=True)

    growth_stage = indexes.MultiValueField(indexed=True, stored=True)

    has_jobs = indexes.BooleanField(indexed=True, stored=True)
    jobs_role = indexes.MultiValueField(indexed=True, stored=True)
    jobs_position = indexes.MultiValueField(indexed=True, stored=True)
    jobs_salary_min = indexes.MultiValueField(indexed=True, stored=True)
    jobs_salary_max = indexes.MultiValueField(indexed=True, stored=True)
    jobs_skill_set = indexes.MultiValueField(indexed=True, stored=True)

    has_relation = indexes.BooleanField(indexed=True, stored=True, default=True)
    is_published = indexes.BooleanField(indexed=True, stored=True)

    popular = indexes.DecimalField(indexed=True, stored=True)



    class Meta:
        model = Organization


    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter()

    def prepare_is_published(self, object):
        # is_published = indexes.BooleanField(indexed=True, stored=True)
        return bool(object.status > 0) and not object.is_deleted

    def prepare_type_of_needs(self, object):
        return [inst.permalink for inst in object.type_of_needs.all()]

    def prepare_type_of_supports(self, object):
        return [inst.permalink for inst in object.type_of_supports.all()]

    def prepare_topics(self, object):
        return [inst.permalink for inst in object.topics.all()]

    def prepare_organization_roles(self, object):
        return [inst.permalink for inst in object.organization_roles.all()]

    def prepare_country(self, object):

        if object.country:
            return object.country.permalink
        else:
            return ''

    def prepare_organization_primary_role(self, object):

        if object.organization_primary_role:
            return object.organization_primary_role.permalink
        else:
            return ''

    def prepare_organization_types(self, object):
        return [inst.permalink for inst in object.organization_types.all()]

    def prepare_investor_types(self, object):
        return [inst.permalink for inst in object.investor_types.all()]

    def prepare_product_launch(self, object):
        if object.product_launch:
            return object.product_launch.permalink
        else:
            return ''

    def prepare_funding(self, object):
        if object.funding:
            return object.funding.permalink
        else:
            return ''

    def prepare_request_funding(self, object):
        if object.request_funding:
            return object.request_funding.permalink
        else:
            return ''

    def prepare_growth_stage(self, object):
        return [inst.permalink for inst in object.growth_stage.all()]

    def prepare_has_jobs(self, object):
        return bool(object.jobs.all().count())

    def prepare_jobs_role(self, object):
        return [inst.role for inst in object.jobs.all()]

    def prepare_jobs_position(self, object):
        return [inst.position for inst in object.jobs.all()]

    def prepare_jobs_salary_min(self, object):
        return [inst.salary_min for inst in object.jobs.all()]

    def prepare_jobs_salary_max(self, object):
        return [inst.salary_max for inst in object.jobs.all()]

    def prepare_jobs_skill_set(self, object):

        skill_set = set([])
        for inst in object.jobs.all():
            for skill in inst.skill_set.all():
                skill_set |= set([skill.name])
        return list(skill_set)

    def prepare_popular(self, object):
        return object.popular



class JobIndex(indexes.ModelSearchIndex, indexes.Indexable):

    content_type = indexes.CharField(default='Job')
    country = indexes.CharField(indexed=True, stored=True)

    has_relation = indexes.BooleanField(indexed=True, stored=True, default=True)
    is_published = indexes.BooleanField(indexed=True, stored=True)


    class Meta:
        model = Job

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter()

    def prepare_is_published(self, object):
        return bool(object.status > 0)

    def prepare_position(self, object):
        return object.get_position_display()

    def prepare_role(self, object):
        return object.get_role_display()

    def prepare_country(self, object):

        if object.country:
            return object.country.permalink
        else:
            return ''