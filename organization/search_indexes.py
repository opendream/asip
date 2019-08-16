import datetime
from decimal import Decimal
from haystack import indexes
from common.constants import STATUS_PUBLISHED
from common.functions import convert_money
from organization.models import Organization, Job, Program

class MultiValueDecimalField(indexes.MultiValueField):
    field_type = 'decimal'

class MultiValueIntegerField(indexes.MultiValueField):
    field_type = 'integer'

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
    investor_type = indexes.CharField(indexed=True, stored=True)
    funding = indexes.CharField(indexed=True, stored=True)
    request_funding = indexes.CharField(indexed=True, stored=True)

    growth_stage = indexes.MultiValueField(indexed=True, stored=True)

    has_jobs = indexes.BooleanField(indexed=True, stored=True)
    jobs_role = indexes.MultiValueField(indexed=True, stored=True)
    jobs_position = indexes.MultiValueField(indexed=True, stored=True)
    jobs_salary_min = indexes.MultiValueField(indexed=True, stored=True)
    jobs_salary_max = indexes.MultiValueField(indexed=True, stored=True)
    jobs_money_salary_min_thb = MultiValueIntegerField(indexed=True, stored=True)
    jobs_money_salary_max_thb = MultiValueIntegerField(indexed=True, stored=True)
    jobs_money_salary_min_usd = MultiValueIntegerField(indexed=True, stored=True)
    jobs_money_salary_max_usd = MultiValueIntegerField(indexed=True, stored=True)
    jobs_equity_min = MultiValueIntegerField(indexed=True, stored=True)
    jobs_equity_max = MultiValueIntegerField(indexed=True, stored=True)
    jobs_skill_set = indexes.MultiValueField(indexed=True, stored=True)
    jobs_job_primary_role = indexes.MultiValueField(indexed=True, stored=True)
    jobs_job_roles =  indexes.MultiValueField(indexed=True, stored=True)
    jobs_locations = indexes.MultiValueField(indexed=True, stored=True)


    has_relation = indexes.BooleanField(indexed=True, stored=True, default=True)
    is_published = indexes.BooleanField(indexed=True, stored=True)

    popular = indexes.DecimalField(indexed=True, stored=True)

    ############## New For 2018 ######################
    focus_sector = indexes.MultiValueField(indexed=True, stored=True)
    focus_industry = indexes.MultiValueField(indexed=True, stored=True)
    stage_of_participants = indexes.MultiValueField(indexed=True, stored=True)
    funding_type = indexes.MultiValueField(indexed=True, stored=True)
    financial_source = indexes.MultiValueField(indexed=True, stored=True)
    attachments_types = indexes.MultiValueField(indexed=True, stored=True)
    assistance_organization = indexes.MultiValueField(indexed=True, stored=True)
    investment_stage_type = indexes.MultiValueField(indexed=True, stored=True)

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

    def prepare_investor_type(self, object):
        if object.investor_type:
            return object.investor_type.permalink
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

    def prepare_jobs_money_salary_min_thb(self, object):
        return [inst.money_salary_min_thb and int(inst.money_salary_min_thb * Decimal('100')) for inst in object.jobs.all()]

    def prepare_jobs_money_salary_max_thb(self, object):
        return [inst.money_salary_max_thb and int(inst.money_salary_max_thb * Decimal('100')) for inst in object.jobs.all()]

    def prepare_jobs_money_salary_min_usd(self, object):
        return [inst.money_salary_min_usd and int(inst.money_salary_min_usd * Decimal('100')) for inst in object.jobs.all()]

    def prepare_jobs_money_salary_max_usd(self, object):
        return [inst.money_salary_max_usd and int(inst.money_salary_max_usd * Decimal('100')) for inst in object.jobs.all()]

    def prepare_jobs_equity_min(self, object):
        return [inst.equity_min and int(inst.equity_min * Decimal('100')) for inst in object.jobs.all()]

    def prepare_jobs_equity_max(self, object):
        return [inst.equity_max and int(inst.equity_max * Decimal('100')) for inst in object.jobs.all()]

    def prepare_jobs_skill_set(self, object):

        skill_set = set([])
        for inst in object.jobs.all():
            for skill in inst.skill_set.all():
                skill_set |= set([skill.name])
        return list(skill_set)

    def prepare_jobs_job_primary_role(self, object):
        items = []
        for inst in object.jobs.all():
            if inst.job_primary_role:
                items.append(inst.job_primary_role.permalink)
                items.append(inst.job_primary_role.permalink)
                items.append(inst.job_primary_role.permalink)
            if inst.job_roles and inst.job_roles.exists():
                for r in inst.job_roles.all():
                    items.append(r.permalink)

        return items

    def prepare_jobs_locations(self, object):
        items = []
        for inst in object.jobs.all():
            for item in inst.locations.all():
                items.append(item.permalink)

        return items

    def prepare_jobs_money_salary_min(self, object):
        return [inst.money_salary_min for inst in object.jobs.all()]

    def prepare_jobs_money_salary_max(self, object):
        return [inst.money_salary_max for inst in object.jobs.all()]

    def prepare_popular(self, object):
        return object.popular

    ############## New For 2018 ######################
    def prepare_focus_sector(self, object):
        return [inst.permalink for inst in object.focus_sector.all()]

    def prepare_focus_industry(self, object):
        return [inst.permalink for inst in object.focus_industry.all()]

    def prepare_stage_of_participants(self, object):
        return [inst.permalink for inst in object.stage_of_participants.all()]

    def prepare_funding_type(self, object):
        return [inst.permalink for inst in object.funding_type.all()]

    def prepare_financial_source(self, object):
        return [inst.permalink for inst in object.financial_source.all()]

    def prepare_attachments_types(self, object):
        return [inst.permalink for inst in object.attachments_types.all()]

    def prepare_assistance_organization(self, object):
        return [inst.assistance.permalink for inst in object.assistance_organization.filter(is_required=True)]

    def prepare_investment_stage_type(self, object):
        try:
            if object.program:
                return [inst.permalink for inst in object.program.investment_stage_type.all()]
        except Program.DoesNotExist:
            pass
        return []


class JobIndex(indexes.ModelSearchIndex, indexes.Indexable):

    content_type = indexes.CharField(default='Job')
    country = indexes.CharField(indexed=True, stored=True)

    has_relation = indexes.BooleanField(indexed=True, stored=True, default=True)
    is_published = indexes.BooleanField(indexed=True, stored=True)

    job_primary_role = indexes.CharField(indexed=True, stored=True)
    job_roles =  indexes.MultiValueField(indexed=True, stored=True)
    locations = indexes.MultiValueField(indexed=True, stored=True)

    money_salary_min_thb = indexes.IntegerField(indexed=True, stored=True)
    money_salary_max_thb = indexes.IntegerField(indexed=True, stored=True)
    money_salary_min_usd = indexes.IntegerField(indexed=True, stored=True)
    money_salary_max_usd = indexes.IntegerField(indexed=True, stored=True)


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

    def prepare_job_primary_role(self, object):
        return object.job_primary_role and object.job_primary_role.permalink

    def prepare_job_roles(self, object):
        return [inst.permalink for inst in object.job_roles.all()]

    def prepare_locations(self, object):
        return [inst.permalink for inst in object.locations.all()]

    def prepare_money_salary_min_thb(self, object):
        return object.money_salary_min_thb and int(object.money_salary_min_thb * Decimal('100'))

    def prepare_money_salary_max_thb(self, object):
        return object.money_salary_max_thb and int(object.money_salary_max_thb * Decimal('100'))

    def prepare_money_salary_min_usd(self, object):
        return object.money_salary_min_usd and int(object.money_salary_min_usd * Decimal('100'))

    def prepare_money_salary_max_usd(self, object):
        return object.money_salary_max_usd and int(object.money_salary_max_usd * Decimal('100'))


class ProgramIndex(indexes.ModelSearchIndex, indexes.Indexable):
    content_type = indexes.CharField(default='Program')

    name = indexes.CharField(indexed=True, stored=True)
    program_type = indexes.MultiValueField(indexed=True, stored=True)

    date_of_establishment = indexes.DateField(indexed=True, stored=True)

    investment_type = indexes.MultiValueField(indexed=True, stored=True)
    investment_stage_type = indexes.MultiValueField(indexed=True, stored=True)

    focus_sector = indexes.MultiValueField(indexed=True, stored=True)
    focus_industry = indexes.MultiValueField(indexed=True, stored=True)
    stage_of_participants = indexes.MultiValueField(indexed=True, stored=True)

    amount_of_financial_supports = indexes.CharField(indexed=True, stored=True)

    organization_id = indexes.IntegerField(indexed=True, stored=True)
    organization_name = indexes.CharField(indexed=True, stored=True)

    class Meta:
        model = Program

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter()

    def prepare_organization_id(self, obj):
        return (obj.organization and obj.organization.id) or None

    def prepare_organization_name(self, obj):
        return (obj.organization and obj.organization.name) or None