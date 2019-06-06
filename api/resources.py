import json
import shlex
import urllib
import bleach
from datetime import timedelta
import datetime
from dateutil import rrule
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import intword, intcomma
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, PermissionDenied
from django.core.paginator import InvalidPage, Paginator as DjangoPaginator
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, Max, Sum, Count, QuerySet
from django.forms import model_to_dict
from django.http import Http404
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from haystack.backends import SQ
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
import sys
from tagging.models import Tag
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.cache import NoCache
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.http import HttpMultipleChoices, HttpGone
from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from tastypie.utils import trailing_slash
from tastypie.paginator import Paginator
from account.functions import user_can_edit, user_can_update_status

from account.models import User
from common.constants import STATUS_PUBLISHED, STATUS_PENDING, STATUS_DRAFT, STATUS_REJECTED
from notification.models import Notification
from organization.models import Organization, Job
from party.models import Party, Portfolio
from presentation.views import get_summary
from relation.models import PartySupportParty, PartyPartnerParty, \
    PartyFollowParty, PartyContactParty, PartyTestifyParty, OrganizationHasPeople, UserExperienceOrganization, PartyLove, \
    PartyReceivedFundingParty, PartyInviteTestifyParty, PartyReceivedInvestingParty, PartyInvestParty, CmsHasParty
from taxonomy.models import Topic, TypeOfNeed, TypeOfSupport, Interest, UserRole, Country, OrganizationRole, OrganizationType, \
    OrganizationProductLaunch, OrganizationFunding, OrganizationGrowthStage, ArticleCategory, InvestorType
from cms.models import News, Event, CommonCms

from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized, NotFound, ApiFieldError
from tastypie.exceptions import BadRequest
from django.utils import six
from django.utils import timezone

class VerboseSerializer(Serializer):
    """
    Gives message when loading JSON fails.
    """
    # Tastypie>=0.9.6,<=0.11.0
    def from_json(self, content):
        """
        Override method of `Serializer.from_json`. Adds exception message when loading JSON fails.
        """
        try:
            return json.loads(content)
        except ValueError as e:
            raise BadRequest(u"Incorrect JSON format: Reason: \"{}\" (See www.json.org for more info.)".format(e.message))


class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # TODO : can see draft pendding status
        return object_list

    def read_detail(self, object_list, bundle):

        return (hasattr(bundle.obj, 'status') and bundle.obj.status in [STATUS_PUBLISHED]) or \
               (hasattr(bundle.obj, 'is_active') and bundle.obj.is_active) or \
               user_can_edit(bundle.request, bundle.obj, bypass_created=True) or \
               (hasattr(bundle.obj, 'REQUIRED_APPROVAL') and bundle.obj.REQUIRED_APPROVAL and user_can_update_status(bundle.request, bundle.obj, bundle.data))


    def create_list(self, object_list, bundle):

        if bundle.request.user.is_authenticated():
            return object_list
        return []

    def create_detail(self, object_list, bundle):
        return bundle.request.user.is_authenticated()

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if user_can_edit(bundle.request, obj, bypass_created=True):
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        result = user_can_update_status(bundle.request, bundle.obj, bundle.data) or \
            user_can_edit(bundle.request, bundle.obj, bypass_created=True)
        return result

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")


class StaffAuthorization(UserAuthorization):

    def create_list(self, object_list, bundle):
        if bundle.request.user.is_staff():
            return object_list
        return []


    def create_detail(self, object_list, bundle):
        return bundle.request.user.is_staff()



class BaseResource(ModelResource):

    def get_schema(self, request, **kwargs):
        """
        Returns a serialized form of the schema of the resource.

        Calls ``build_schema`` to generate the data. This method only responds
        to HTTP GET.

        Should return a HttpResponse (200 OK).
        """
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        bundle = self.build_bundle(request=request)
        self.authorized_read_detail(self.get_object_list(bundle.request), bundle)
        return self.create_response(request, self.build_schema(request=request))

    def build_schema(self, request=None):
        base_schema = super(BaseResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })

        route = request.GET.get('route')
        if route:
            for key in route.split('.'):
                base_schema = base_schema[key]

            dict_map = request.GET.get('dict_map')
            if dict_map:

                dict_map = dict_map.split(',')
                base_schema = {'objects': [dict(zip(dict_map, item)) for item in base_schema]}

        return base_schema


    def dehydrate(self, bundle):

        bundle.data['can_edit'] = user_can_edit(bundle.request, bundle.obj, bypass_created=True)

        return bundle


    def get_result(self, request, **kwargs):
        """
        Returns a single serialized resource.

        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        basic_bundle = self.build_bundle(request=request)

        obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle, for_list=True)
        bundle = self.alter_detail_data_to_serialize(request, bundle)

        desired_format = self.determine_format(request)
        serialized = self.serialize(request, bundle, desired_format)

        return serialized


class BaseVaryStatusResource(ModelResource):

    def obj_get_list(self, bundle, **kwargs):

        # TODO: check draft pending with user logged in
        kwargs['status'] = STATUS_PUBLISHED
        kwargs['is_active'] = True
        return super(BaseVaryStatusResource, self).obj_get_list(bundle, **kwargs)


class ToManyFieldForList(fields.ToManyField):

    def dehydrate_related(self, bundle, related_resource, for_list=True):

        should_dehydrate_full_resource = self.should_full_dehydrate(bundle, for_list=for_list)

        if not should_dehydrate_full_resource:
            # Be a good netizen.
            return related_resource.get_resource_uri(bundle)
        else:
            # ZOMG extra data and big payloads.
            bundle = related_resource.build_bundle(
                obj=bundle.obj,
                request=bundle.request,
                objects_saved=bundle.objects_saved
            )
            return related_resource.full_dehydrate(bundle, for_list=True)

class TopicResource(BaseResource):

    #childrens = fields.ToManyField('self', 'children', null=True, full=True)
    parent = fields.ToOneField('self', 'parent', null=True)

    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = Topic.objects.filter(level=0).order_by('title')
        resource_name = 'topic'
        filtering = {
            'level': ALL,
            'childrens': ALL_WITH_RELATIONS,
            'permalink': ALL
        }

class TopicItemResource(BaseResource):

    parent = fields.ToOneField('self', 'parent', null=True)

    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = Topic.objects.order_by('title')
        resource_name = 'topic_item'
        filtering = {
            'level': ALL,
            'childrens': ALL_WITH_RELATIONS,
            'permalink': ALL
        }

class ArticleCategoryItemResource(BaseResource):

    parent = fields.ToOneField('self', 'parent', null=True)

    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = ArticleCategory.objects.all().order_by('-priority', 'id')
        resource_name = 'article_category_item'
        filtering = {
            'level': ALL,
            'childrens': ALL_WITH_RELATIONS,
            'permalink': ALL,
            'parent': ALL_WITH_RELATIONS
        }

class TypeOfNeedResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = TypeOfNeed.objects.all()
        resource_name = 'type_of_need'
        filtering = {
            'permalink': ALL,
            'priority': ALL
        }

class TypeOfSupportResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = TypeOfSupport.objects.all()
        resource_name = 'type_of_support'
        filtering = {
            'permalink': ALL,
            'priority': ALL,
        }

class InterestResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = Interest.objects.all()
        resource_name = 'interest'
        filtering = {
            'permalink': ALL,
        }

class UserRoleResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = UserRole.objects.all()
        resource_name = 'user_role'
        filtering = {
            'permalink': ALL,
        }

class OrganizationRoleResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = OrganizationRole.objects.all()
        resource_name = 'organization_role'
        filtering = {
            'permalink': ALL,
        }

class CountryResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = Country.objects.all()
        resource_name = 'country'
        filtering = {
            'permalink': ALL,
        }

class OrganizationTypeResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = OrganizationType.objects.all()
        resource_name = 'organization_type'
        filtering = {
            'permalink': ALL,
        }
        include_absolute_url = True

class InvestorTypeResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = InvestorType.objects.all()
        resource_name = 'investor_type'
        filtering = {
            'permalink': ALL,
        }

class OrganizationProductLaunchResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = OrganizationProductLaunch.objects.all()
        resource_name = 'organization_product_launch'
        filtering = {
            'permalink': ALL,
        }

class OrganizationFundingResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = OrganizationFunding.objects.all()
        resource_name = 'organization_funding'
        filtering = {
            'permalink': ALL,
        }

class OrganizationGrowthStageResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = OrganizationGrowthStage.objects.all()
        resource_name = 'organization_growth_stage'
        filtering = {
            'permalink': ALL,
        }


preserve_keys = [
    'q', 'page', 'limit', 'offset', 'resource', 'none_to_all', 'content_type', 'order_by',
    'roles', 'created__year__lte', 'created__month__lte', 'is_published', 'include_unpublished',
]

def base_get_search(self, request, model=None, for_list=True, get_queryset=False, **kwargs):

    self.method_check(request, allowed=['get'])
    self.is_authenticated(request)
    self.throttle_check(request)

    # Do the query.
    #params = dict(request.GET)
    params = {}
    params = request.GET.dict()

    sq = None
    keywords = request.GET.get('q', '')
    keywords = keywords.strip() or '*'
    keywords = urllib.unquote(keywords).decode('utf8').replace('+', ' ').lower()

    none_to_all = request.GET.get('none_to_all', False)

    for phrase in shlex.split(keywords):
        if not sq:
            sq = SQ(content=phrase)
        else:
            sq |= SQ(content=phrase)

    params_sq = None

    for key, values in request.GET.iterlists():

        if key in preserve_keys:
            continue

        param_sq = None
        for value in values:

            if not param_sq:
                param_sq = SQ(**{key: value})
            else:
                param_sq |= SQ(**{key: value})

        if not params_sq:
            params_sq = param_sq
        else:
            params_sq &= param_sq


    if request.GET.get('created__year__lte'):
        now = datetime.datetime.now()

        created = {}

        created['year'] = int(request.GET.get('created__year__lte'))

        if request.GET.get('created__month__lte'):
            created['month'] = int(request.GET.get('created__month__lte'))
        else:
            created['month'] = now.month
        created['month'] += 1

        created['day'] = 1

        while created['month'] > 12:
            created['month'] -= 12
            created['year'] += 1

        created__lte = datetime.datetime(**created) - timedelta(days=1)

        if not params_sq:
            params_sq = SQ(created__lte=created__lte)
        else:
            params_sq &= SQ(created__lte=created__lte)




    if request.GET.get('roles'):

        role = request.GET.get('roles')

        param_sq = SQ(organization_roles=role) | SQ(user_roles=role)
        if not params_sq:
            params_sq = param_sq
        else:
            params_sq &= param_sq


    if none_to_all and keywords == '*':
        sqs = SearchQuerySet().all()
    else:
        sqs = SearchQuerySet().filter(sq)

    content_type = (model and model.__name__) or request.GET.get('content_type')
    if content_type:
        sqs = sqs.filter(content_type=content_type)

    if params_sq:
        sqs = sqs.filter(params_sq)


    if keywords == '*':
        sqs = sqs.order_by('-store_popular', '-created')

    if not request.GET.get('include_unpublished', False):
        sqs = sqs.filter(is_published=True)

    if get_queryset:
        return sqs

    total_count = sqs.count()


    # Manual pager for fixed the bug
    limit = int(request.GET.get('limit', 20))
    page = int(request.GET.get('page', 1)) - 1
    offset = int(request.GET.get('offset', 0))

    if not offset:
        offset = page*limit

    object_list = sqs[offset:(offset+limit)]


    objects = []

    resource = request.GET.get('resource', False)
    if not resource:
        resource = self
    else:
        resource = getattr(sys.modules[__name__], resource)()

    for result in object_list:


        bundle = self.build_bundle(obj=result.object, request=request)
        bundle = resource.full_dehydrate(bundle, for_list=for_list)
        objects.append(bundle)


    object_list = {
        'meta': {
            'total_count': total_count,
            'has_next': total_count > limit
        },
        'objects': objects,
    }

    self.log_throttled_access(request)
    return self.create_response(request, object_list)


class SkillResource(BaseResource):

    class Meta:
        allowed_methods = ['get']
        queryset = Tag.objects.all()
        resource_name = 'skill'
        filtering = {
            'name': ALL,
        }


class NewsTagResource(Resource):

    id = fields.CharField(attribute='id')
    name = fields.CharField(attribute='name')
    num_items = fields.CharField(attribute='num_items')

    class Meta:
        allowed_methods = ['get']
        resource_name = 'news_tag'
        object_class = None


    def get_object_list(self, request):
        categories = request.GET.get('categories')
        if categories:
            queryset = Tag.objects.raw('''
            SELECT tagging_tag.id, tagging_tag.name, COUNT(tagging_taggeditem.id) AS num_items
            FROM tagging_tag
            INNER JOIN tagging_taggeditem ON ( tagging_tag.id = tagging_taggeditem.tag_id )
            INNER JOIN cms_news ON ( tagging_taggeditem.object_id = cms_news.commoncms_ptr_id )
            INNER JOIN cms_news_categories ON ( cms_news.commoncms_ptr_id = cms_news_categories.news_id)
            INNER JOIN taxonomy_articlecategory ON ( cms_news_categories.articlecategory_id = taxonomy_articlecategory.id)
            WHERE tagging_taggeditem.content_type_id = %d AND taxonomy_articlecategory.permalink = '%s'
            GROUP BY tagging_tag.id
            HAVING COUNT("tagging_taggeditem"."id") > 0
            ORDER BY num_items DESC
            LIMIT 50
            ''' % (ContentType.objects.get_for_model(News).id, categories))
            return [row for row in queryset]

        return []
    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)


class EventTagResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Tag.objects.filter(items__content_type=ContentType.objects.get_for_model(Event)).annotate(
            num_items=Count('items')).filter(num_items__gt=0).order_by('-num_items')
        resource_name = 'event_tag'
        filtering = {
        }

class JobTagResource(BaseResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Tag.objects.filter(items__content_type=ContentType.objects.get_for_model(Job)).annotate(
            num_items=Count('items')).filter(num_items__gt=0).order_by('-num_items')
        resource_name = 'job_tag'
        filtering = {
            'name': ALL
        }

class PartyResource(BaseResource, BaseVaryStatusResource):

    ordering = fields.IntegerField(attribute='_ordering')


    portfolios = fields.ToManyField('api.resources.PortfolioResource', 'portfolios',
                                    null=True, blank=True, use_in='detail')

    get_thumbnail = fields.CharField(attribute='get_thumbnail')
    get_thumbnail_in_primary = fields.CharField(attribute='get_thumbnail_in_primary')
    get_display_name = fields.CharField(attribute='get_display_name')
    get_short_name = fields.CharField(attribute='get_short_name')
    get_summary = fields.CharField(attribute='get_summary')
    get_status = fields.IntegerField(attribute='get_status')

    country = fields.ForeignKey('api.resources.CountryResource', 'country',
                                   related_name='country', null=True, blank=True,
                                   full=True)

    inst_type = fields.CharField(attribute='inst_type')

    total_follower = fields.IntegerField(attribute='total_follower', null=True, blank=True)
    total_following = fields.IntegerField(attribute='total_following', null=True, blank=True)
    total_love = fields.IntegerField(attribute='total_love', null=True, blank=True)
    total_testify = fields.IntegerField(attribute='total_testify', null=True, blank=True)

    total_views = fields.IntegerField(attribute='total_views', null=True, blank=True)
    popular = fields.DecimalField(attribute='popular', null=True, blank=True)


    class Meta:
        allowed_methods = ['get']
        queryset = Party.objects.all()
        resource_name = 'party'
        include_absolute_url = True

        excludes = ['store_total_follower', 'store_total_following', 'store_total_love', 'store_total_testify']

        filtering = {
            'id': ALL,
        }

    def prepend_urls(self):
        '^(?P<username>[\w.@+-]+)/(?P<people_id>\d+)/$'
        return [
            url(r"^(?P<resource_name>%s)/(?P<party_id>\d+)/partners/$" % (self._meta.resource_name),
                self.wrap_view('get_partners'), name="api_get_partners"),
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),

        ]

    def get_partners(self, request, party_id, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        limit = request.GET.get('limit') or 20
        ordering__lt = request.GET.get('ordering__lt') or 9999999999

        sqs = Party.objects.filter(
            (Q(partner_dst__src__id=party_id) | Q(partner_src__dst__id=party_id)) &
            (Q(organization__ordering__lt=ordering__lt) | Q(user__ordering__lt=ordering__lt)))\
            .order_by('-organization__ordering', '-user__ordering').distinct()\
            .extra(select={'approval_status': 'relation_partypartnerparty.status'})

        total_count = sqs.count()

        paginator = DjangoPaginator(sqs, limit)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for object in page.object_list:
            bundle = self.build_bundle(obj=object, request=request)

            bundle.data['REQUIRED_APPROVAL'] = PartyPartnerParty.REQUIRED_APPROVAL
            bundle.data['approval_status'] = object.approval_status

            bundle = self.full_dehydrate(bundle, for_list=True)
            objects.append(bundle)

        object_list = {
            'meta': {
                'limit': limit,
                'total_count': total_count
            },
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


    def get_search(self, request, model=None, **kwargs):
        return base_get_search(self, request, model, **kwargs)

    def dehydrate(self, bundle):

        bundle = super(PartyResource, self).dehydrate(bundle)

        if bundle.data.get('party_ptr'):
            bundle.data['party_resource_uri'] = bundle.data['party_ptr']
        else:
            bundle.data['party_resource_uri'] = self.get_resource_uri(bundle)


        bundle.data['is_following'] = False
        bundle.data['is_love'] = False
        bundle.data['can_following'] = False
        bundle.data['can_love'] = False

        if bundle.request.user.is_authenticated():
            bundle.data['can_following'] = True
            bundle.data['can_love'] = True

            bundle.data['is_following'] = bundle.obj.is_following(bundle.request.logged_in_party)
            bundle.data['is_love'] = bundle.obj.is_love(bundle.request.logged_in_party)
        return bundle


class UserResource(PartyResource):

    ordering = fields.IntegerField(attribute='ordering')
    party_ptr = fields.ToOneField('api.resources.PartyResource', 'party_ptr')

    description = fields.CharField(attribute='description', null=True, blank=True, use_in='detail')
    interests = fields.ToManyField('api.resources.TopicResource', 'interests', related_name='interests',
                                   null=True, blank=True, full=True, use_in='detail')
    user_roles = fields.ToManyField('api.resources.UserRoleResource', 'user_roles', related_name='user_roles',
                                    null=True, blank=True, full=True, use_in='detail')
    admins = fields.ManyToManyField('api.resources.PartyResource', 'admins', related_name='admins',
                                    null=True, blank=True, full=True, use_in='detail')

    skill_set = fields.ManyToManyField('api.resources.SkillResource', 'skill_set', related_name='skill_set',
                                       null=True, blank=True, full=True, use_in='detail')


    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        detail_uri_name = 'username'
        queryset = User.objects.filter(is_deleted=False).order_by('-ordering')
        resource_name = 'user'
        include_absolute_url = True

        excludes = ['store_total_follower', 'store_total_following', 'store_total_love', 'store_total_testify', 'password', 'email', 'image']

        paginator_class = Paginator
        filtering = {
            'user_roles': ALL_WITH_RELATIONS,
            'interests': ALL_WITH_RELATIONS,
            'id': ALL,
            'ordering': ALL,
            'is_active': ALL,
            'country': ALL_WITH_RELATIONS,
            'skill_set': ALL_WITH_RELATIONS,
            'skills': ALL
        }
        ordering = ['ordering', 'id', 'priority']


    def get_search(self, request, **kwargs):
        return base_get_search(self, request, get_user_model(), **kwargs)

    def obj_get_list(self, bundle, **kwargs):
        # TODO: check draft pending with user logged in
        kwargs['id__gt'] = 1
        return super(UserResource, self).obj_get_list(bundle, **kwargs)

class UserLiteResource(UserResource):

    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        detail_uri_name = 'username'
        queryset = User.objects.filter(is_deleted=False).order_by('-ordering')
        resource_name = 'user'
        include_absolute_url = True

        fields = ['store_total_follower', 'store_total_following', 'store_total_love', 'store_total_testify',
                    'password', 'email', 'image']

        paginator_class = Paginator
        filtering = {
            'user_roles': ALL_WITH_RELATIONS,
            'interests': ALL_WITH_RELATIONS,
            'id': ALL,
            'ordering': ALL,
            'is_active': ALL,
            'country': ALL_WITH_RELATIONS,
            'skill_set': ALL_WITH_RELATIONS,
            'skills': ALL
        }
        ordering = ['ordering', 'id', 'priority']


class OrganizationResource(PartyResource):

    get_thumbnail_images = fields.ListField(attribute='get_thumbnail_images' ,null=True, blank=True, use_in='detail')

    ordering = fields.IntegerField(attribute='ordering')
    party_ptr = fields.ToOneField('api.resources.PartyResource', 'party_ptr')

    TYPE_SOCIAL_ENTERPRISE = fields.CharField(attribute='TYPE_SOCIAL_ENTERPRISE')
    TYPE_STARTUP = fields.CharField(attribute='TYPE_STARTUP')
    TYPE_SUPPORTING_ORGANIZATION = fields.CharField(attribute='TYPE_SUPPORTING_ORGANIZATION')

    description = fields.CharField(attribute='description', null=True, blank=True, use_in='detail')
    type_of_needs = fields.ToManyField('api.resources.TypeOfNeedResource', 'type_of_needs',
                                       related_name='type_of_needs', null=True, blank=True,
                                       full=True, use_in='detail')
    type_of_supports = fields.ToManyField('api.resources.TypeOfSupportResource', 'type_of_supports',
                                          related_name='type_of_supports', null=True, blank=True,
                                          full=True, use_in='detail')
    topics = fields.ToManyField('api.resources.TopicItemResource', 'topics', related_name='topics',
                                null=True, blank=True, full=True, use_in='detail')

    organization_primary_role = fields.ForeignKey('api.resources.OrganizationRoleResource', 'organization_primary_role', related_name='organization_primary_role',
                                            null=True, blank=True, full=True)

    organization_roles = fields.ToManyField('api.resources.OrganizationRoleResource', 'organization_roles',
                                            related_name='organization_roles',
                                            null=True, blank=True, full=True)

    organization_types = fields.ToManyField('api.resources.OrganizationTypeResource', 'organization_types',
                                related_name='organization_types', null=True, blank=True,
                                full=True)

    investor_types = fields.ToManyField('api.resources.InvestorTypeResource', 'investor_types',
                                          related_name='investor_types', null=True, blank=True,
                                          full=True)

    product_launch = fields.ForeignKey('api.resources.OrganizationProductLaunchResource', 'product_launch',
                                       related_name='product_launch', null=True, blank=True,
                                       full=True)

    funding = fields.ForeignKey('api.resources.OrganizationFundingResource', 'funding',
                                       related_name='funding', null=True, blank=True,
                                       full=True)

    request_funding = fields.ForeignKey('api.resources.OrganizationFundingResource', 'request_funding',
                                related_name='request_funding', null=True, blank=True,
                                full=True)

    growth_stage = fields.ToManyField('api.resources.OrganizationGrowthStageResource', 'growth_stage',
                                            related_name='growth_stage',
                                            null=True, blank=True, full=True)
    #jobs = ToManyFieldForList('api.resources.JobResource', 'jobs',
    #                                full=True, null=True, blank=True, use_in='detail')


    # Choice fields
    gender_of_representative = fields.CharField(attribute='get_gender_of_representative_display', use_in='detail')
    legal_structure = fields.CharField(attribute='get_legal_structure_display', use_in='detail')
    target_beneficiary = fields.CharField(attribute='get_target_beneficiary_display', use_in='detail')
    client_type = fields.CharField(attribute='get_client_type_display', use_in='detail')
    annual_revenue = fields.CharField(attribute='get_annual_revenue_display', use_in='detail')
    revenue_model = fields.CharField(attribute='get_revenue_model_display', use_in='detail')
    possible_form_of_financial_support = fields.CharField(attribute='get_possible_form_of_financial_support_display', use_in='detail')
    potential_use_of_investment = fields.CharField(attribute='get_potential_use_of_investment_display', use_in='detail')
    possible_form_of_non_financial_support = fields.CharField(attribute='get_possible_form_of_non_financial_support_display', use_in='detail')


    # Sections
    sector_activities = fields.ToManyField('api.resources.TopicItemResource', 'sector_activities', related_name='sector_activities',
                                           null=True, blank=True, full=True, use_in='detail')
    productservice_type = fields.ToManyField('api.resources.TopicItemResource', 'productservice_type', related_name='productservice_type',
                                             null=True, blank=True, full=True, use_in='detail')

    client_locations = fields.ToManyField('api.resources.CountryResource', 'client_locations', related_name='client_locations',
                                             null=True, blank=True, full=True, use_in='detail')

    # Formset
    team_information = fields.ListField(attribute='team_information', use_in='detail')
    phone_number_of_organizations_headquarters = fields.ListField(attribute='phone_number_of_organizations_headquarters', use_in='detail')
    location_of_organizations_operating_facilities = fields.ListField(attribute='location_of_organizations_operating_facilities', use_in='detail')
    measurement_year_values = fields.ListField(attribute='measurement_year_values', use_in='detail')
    top_3_major_investors_year_and_amount = fields.ListField(attribute='top_3_major_investors_year_and_amount', use_in='detail')
    top_3_major_donors_year_and_amount = fields.ListField(attribute='top_3_major_donors_year_and_amount', use_in='detail')


    class Meta:
        allowed_methods = ['get']
        authorization = UserAuthorization()
        detail_uri_name = 'permalink'
        queryset = Organization.objects.all().order_by('-ordering')

        resource_name = 'organization'
        include_absolute_url = True
        excludes = ['changed', 'created', 'created_raw', 'is_deleted', 'published',
                    'store_team_information',
                    'store_phone_number_of_organizations_headquarters',
                    'store_location_of_organizations_operating_facilities',
                    'store_measurement_year_values',
                    'store_top_3_major_investors_year_and_amount',
                    'store_top_3_major_donors_year_and_amount',
                    'store_total_follower', 'store_total_following', 'store_total_love', 'store_total_testify']

        filtering = {
            'id': ALL,
            'type_of_organization': ALL,
            'organization_primary_role': ALL_WITH_RELATIONS,
            'organization_roles': ALL_WITH_RELATIONS,
            'country': ALL_WITH_RELATIONS,
            'type_of_needs': ALL_WITH_RELATIONS,
            'type_of_supports': ALL_WITH_RELATIONS,
            'topics': ALL_WITH_RELATIONS,
            'product_launch': ALL_WITH_RELATIONS,
            'funding': ALL_WITH_RELATIONS,
            'request_funding': ALL_WITH_RELATIONS,
            'growth_stage': ALL_WITH_RELATIONS,
            'ordering': ALL,
            'image': ALL,
            'status': ALL,
            'promote': ALL
        }
        ordering = ['ordering', 'id', 'priority', 'order_by_role', 'promote']


    def get_search(self, request, **kwargs):
        return base_get_search(self, request, Organization)



    def get_object_list(self, request):
        query = super(OrganizationResource, self).get_object_list(request)

        order_by_role = request.GET.get('order_by_role')
        if order_by_role:
            order_by_role = OrganizationRole.objects.get(permalink=order_by_role)
            query = query.extra(select={'order_by_role': 'organization_organization.organization_primary_role_id=%d' % order_by_role.id}).order_by('-order_by_role', '-ordering')

        return query


class PartyLiteResource(PartyResource):

    pk = fields.IntegerField(attribute='id')

    topics = fields.ToManyField('api.resources.TopicItemResource', 'topics', related_name='topics',
                                null=True, blank=True, full=True)
    interests = fields.ToManyField('api.resources.TopicItemResource', 'interests', related_name='interests',
                                null=True, blank=True, full=True)
    user_roles = fields.ToManyField('api.resources.UserRoleResource', 'user_roles', related_name='user_roles',
                                    null=True, blank=True, full=True)
    product_launch = fields.ForeignKey('api.resources.OrganizationProductLaunchResource', 'product_launch', related_name='product_launch',
                                null=True, blank=True, full=True)
    funding = fields.ForeignKey('api.resources.OrganizationFundingResource', 'funding',
                                       related_name='funding',
                                       null=True, blank=True, full=True)
    request_funding = fields.ForeignKey('api.resources.OrganizationFundingResource', 'request_funding',
                                related_name='request_funding',
                                null=True, blank=True, full=True)
    organization_types = fields.ToManyField('api.resources.OrganizationTypeResource', 'organization_types',
                                related_name='organization_types',
                                null=True, blank=True, full=True)
    investor_types = fields.ToManyField('api.resources.InvestorTypeResource', 'investor_types',
                                          related_name='investor_types',
                                          null=True, blank=True, full=True)
    growth_stage = fields.ToManyField('api.resources.OrganizationGrowthStageResource', 'growth_stage',
                                      related_name='growth_stage',
                                      null=True, blank=True, full=True)

    deal_size_start = fields.IntegerField(attribute='deal_size_start', null=True, blank=True,)
    deal_size_end = fields.IntegerField(attribute='deal_size_end', null=True, blank=True,)
    deal_size = fields.CharField(null=True, blank=True,)

    get_status = fields.IntegerField(attribute='get_status')

    popular = fields.DecimalField(attribute='popular', null=True, blank=True,)


    class Meta:
        allowed_methods = ['get']
        authorization = UserAuthorization()
        queryset = Party.objects.all().order_by('-ordering')

        resource_name = 'party'
        include_absolute_url = True
        fields = [
            'get_thumbnail', 'get_thumbnail_in_primary', 'get_display_name', 'get_summary', 'topics', 'interests',
            'product_launch', 'funding', 'request_funding', 'image', 'total_love', 'total_follower', 'popular',
            'deal_size_start', 'deal_size_end', 'store_popular'
        ]

    def dehydrate_deal_size(self, bundle):

        try:

            deal_size_start = bundle.obj.deal_size_start or 0
            deal_size_end = bundle.obj.deal_size_end or 0

            if deal_size_start < 1000000:
                deal_size_start = intcomma(deal_size_start)

            if deal_size_end < 1000000:
                deal_size_end = intcomma(deal_size_end)

            if deal_size_start != '0' and deal_size_end != '0':
                return '%s%s - %s%s' % (settings.CURRENCY_SHORT, intword(deal_size_start), settings.CURRENCY_SHORT, intword(deal_size_end))
            elif deal_size_start != '0':
                return '> %s%s' % (settings.CURRENCY_SHORT, intword(deal_size_start))

            elif deal_size_end != '0':
                return '< %s%s' % (settings.CURRENCY_SHORT, intword(deal_size_start))
            else:
                return '-'

        except AttributeError:
            return None


class TagResource(BaseResource):

    #title = fields.CharField(attribute='name', readonly=True)
    #permalink = fields.CharField(attribute='name', readonly=True)

    class Meta:
        allowed_methods = ['get']
        authorization = StaffAuthorization()
        queryset = Tag.objects.order_by('name')
        resource_name = 'tag'
        filtering = {
            'name': ALL
        }


class BaseRelationResource(BaseResource):
    REQUIRED_APPROVAL = fields.BooleanField(attribute='REQUIRED_APPROVAL')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/sum/$" % (self._meta.resource_name),
                self.wrap_view('get_sum_fields'), name="api_get_sum_fields"),
        ]

    def get_sum_fields(self, request, **kwargs):


        bundle = self.build_bundle(request=request)
        queryset = self.obj_get_list(bundle, **kwargs)

        filters = {}

        fields = request.GET.getlist('fields')
        for field in fields:
            filters[field] = Sum(field)

        return self.create_response(request, queryset.aggregate(**filters))


# Relation
class OrganizationHasPeopleResource(BaseRelationResource):
    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True,
                            related_name='organization_has_people_src')

    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True,
                        related_name='organization_has_people_dst')

    class Meta:
        authorization = UserAuthorization()
        always_return_data = True
        queryset = OrganizationHasPeople.objects.all().order_by('id')
        resource_name = 'organization_has_people'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }
        ordering = ['id', 'created', 'changed', 'status']


class PartySupportPartyResource(BaseRelationResource):
    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True,
                            related_name='support_src')
    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True,
                            related_name='support_dst')

    class Meta:
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartySupportParty.objects.all().order_by('id')
        resource_name = 'party_support_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }
        ordering = ['id', 'created', 'changed', 'status']

class PartyInvestPartyResource(BaseRelationResource):
    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True,
                            related_name='invest_src')
    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True,
                            related_name='invest_dst')

    class Meta:
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyInvestParty.objects.all().order_by('id')
        resource_name = 'party_invest_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }
        ordering = ['id', 'created', 'changed', 'status']


class PartyPartnerPartyResource(BaseRelationResource):
    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True,
                            related_name='partner_src')
    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True,
                            related_name='partner_dst')

    class Meta:
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyPartnerParty.objects.all()
        resource_name = 'party_partner_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }


class CmsHasPartyResource(BaseRelationResource):
    #src = fields.ForeignKey('api.resources.CmsResource', 'src', blank=True, full=True,
    #                        related_name='cms_has_party_src')

    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True,
                        related_name='cms_has_party_dst')

    class Meta:
        authorization = UserAuthorization()
        always_return_data = True
        queryset = CmsHasParty.objects.all().order_by('id')
        resource_name = 'cms_has_party'
        filtering = {
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }
        ordering = ['id', 'created', 'changed', 'status']


# Take action

# For create and update

# curl --dump-header - -H "Content-Type: application/json" -X POST --data '{
#     "dst"  : "/api/v1/party/218/",
#     "status": 1
# }' "http://localhost:8000/api/v1/party_follow_party/"

# curl --dump-header - -H "Content-Type: application/json" -X POST --data '{
#     "dst"  : "/api/v1/party/218/",
#     "status": -2
# }' "http://localhost:8000/api/v1/party_follow_party/"

# For update with id

# curl --dump-header - -H "Content-Type: application/json" -X PUT --data '{
#     "status": 1
# }' "http://localhost:8000/api/v1/party_follow_party/5/"

class BasePartySendUniqueDataPartyResource(BaseRelationResource):


    def obj_create(self, bundle, **kwargs):

        bundle.obj = self._meta.object_class()
        ModelClass = type(bundle.obj)

        for key, value in kwargs.items():

            setattr(bundle.obj, key, value)

        bundle.obj.src = bundle.request.logged_in_party


        bundle = self.full_hydrate(bundle)

        if hasattr(bundle.obj, 'dst_content_type'):
            exists = list(ModelClass.objects.filter(src=bundle.request.logged_in_party, dst_id=bundle.obj.dst.id).order_by('id'))
        else:
            exists = list(ModelClass.objects.filter(src=bundle.request.logged_in_party, dst=bundle.obj.dst).order_by('id'))
        if len(exists):

            survivor = exists.pop()
            for exist in exists:
                exist.delete()

            bundle.obj = survivor

        if bundle.data.get('status') is None:
            bundle.data['status'] = STATUS_PUBLISHED

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)

        bundle.obj.src = bundle.request.logged_in_party

        return self.save(bundle)

    def obj_update(self, bundle, skip_errors=False, **kwargs):

        bundle = super(BasePartySendUniqueDataPartyResource, self).obj_update(bundle, skip_errors, **kwargs)
        if bundle.obj.src != bundle.request.logged_in_party:
            bundle.obj.src = bundle.request.logged_in_party
            bundle.obj.save()

        return bundle


class PartyFollowPartyResource(BasePartySendUniqueDataPartyResource):
    # use PartyResource faster than UserResource
    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True)
    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True)

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyFollowParty.objects.all()
        resource_name = 'party_follow_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }
        ordering = ['id']


# Take action
class BasePartySendDataPartyResource(BaseRelationResource):

    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True)
    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True)

    default_status = STATUS_PUBLISHED

    def obj_create(self, bundle, **kwargs):


        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        if bundle.data.get('status') is None:
            bundle.data['status'] = self.default_status

        bundle = self.full_hydrate(bundle)
        bundle.obj.src = bundle.request.logged_in_party

        if not user_can_edit(bundle.request, bundle.obj, bypass_created=True):
            raise PermissionDenied()


        return self.save(bundle)


    def obj_update(self, bundle, skip_errors=False, **kwargs):

        if bundle.data.get('src'):
            del(bundle.data['src'])

        if not bundle.obj or not self.get_bundle_detail_data(bundle):
            try:
                lookup_kwargs = self.lookup_kwargs_with_identifiers(bundle, kwargs)
            except:

                lookup_kwargs = kwargs
            try:
                bundle.obj = self.obj_get(bundle=bundle, **lookup_kwargs)
            except ObjectDoesNotExist:
                raise NotFound("A model instance matching the provided arguments could not be found.")

        bundle = self.full_hydrate(bundle)


        # dst pdate status approve or reject
        if user_can_update_status(bundle.request, bundle.obj, bundle.data):
           pass

        elif not user_can_edit(bundle.request, bundle.obj, bypass_created=True):
            raise PermissionDenied()

        return self.save(bundle, skip_errors=skip_errors)


# Take action
class PartyContactPartyResource(BasePartySendDataPartyResource):

    default_status = PartyContactParty.STATUS_UNREAD

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyContactParty.objects.all().order_by('-id')
        resource_name = 'party_contact_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'system': ALL,
            'status': ALL,
            'id': ALL,
        }
        ordering = ['id']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/new_count/$" % (self._meta.resource_name),
                self.wrap_view('get_new_count'), name="api_get_new_count"),
        ]

    def get_new_count(self, request, **kwargs):

        new_count = 0

        if request.logged_in_party:
            new_count = PartyContactParty.objects.filter(
                status=PartyContactParty.STATUS_UNREAD,
                dst__id=request.logged_in_party.id
            ).count()

        return self.create_response(request, new_count)

# Take action
class PartyTestifyPartyResource(BasePartySendDataPartyResource):

    default_status = STATUS_PENDING

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyTestifyParty.objects.all().order_by('-ordering')
        resource_name = 'party_testify_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'status': ALL,
        }
        ordering = ['-ordering']

class PartyInviteTestifyPartyResource(BasePartySendDataPartyResource):

    default_status = STATUS_PENDING

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyInviteTestifyParty.objects.all().order_by('-created')
        resource_name = 'party_invite_testify_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'status': ALL,
        }
        ordering = ['-created']


class PartyReceivedFundingPartyResource(BasePartySendDataPartyResource):

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyReceivedFundingParty.objects.all().order_by('-ordering')
        resource_name = 'party_received_funding_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'status': ALL,
        }
        ordering = ['-ordering']


class PartyReceivedInvestingPartyResource(BasePartySendDataPartyResource):

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyReceivedInvestingParty.objects.all().order_by('-ordering')
        resource_name = 'party_received_investing_party'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'status': ALL,
        }
        ordering = ['-ordering']

class ContentTypeResource(BaseResource):


    class Meta:
        queryset = ContentType.objects.filter()
        allowed_methods = ['get']
        resource_name = 'content_type'
        filtering = {
            'name': ALL,
            'model': ALL,
            'app_label': ALL
        }


class PortfolioResource(BaseResource):

    get_thumbnails = fields.ListField(attribute='get_thumbnails')
    get_images = fields.ListField(attribute='get_images')

    party_portfolios = fields.ToManyField('api.resources.PartyResource', 'party_portfolios', related_name='party_portfolios', null=True, blank=True)

    class Meta:
        allowed_methods = ['get']
        queryset = Portfolio.objects.all().order_by('-ordering').distinct()
        resource_name = 'portfolio'
        include_absolute_url = True
        filtering = {
            'ordering': ALL,
            'party_portfolios': ALL_WITH_RELATIONS
        }
        ordering = ['ordering', 'id', 'priority']
        excludes = ['changed', 'created', 'is_deleted', 'images']


class JobToManyFieldForList(ToManyFieldForList):

    def dehydrate(self, bundle, for_list=True):
        if not bundle.obj or not bundle.obj.pk:
            if not self.null:
                raise ApiFieldError(
                    "The model '%r' does not have a primary key and can not be used in a ToMany context." % bundle.obj)

            return []

        the_m2ms = None
        previous_obj = bundle.obj
        attr = self.attribute

        if isinstance(self.attribute, six.string_types):
            attrs = self.attribute.replace('job__', 'job_').replace('job_', 'job__').split('__')
            the_m2ms = bundle.obj

            for attr in attrs:
                previous_obj = the_m2ms
                try:
                    the_m2ms = getattr(the_m2ms, attr, None)
                except ObjectDoesNotExist:
                    the_m2ms = None

                if not the_m2ms:
                    break

        elif callable(self.attribute):
            the_m2ms = self.attribute(bundle)

        if not the_m2ms:
            if not self.null:
                raise ApiFieldError(
                    "The model '%r' has an empty attribute '%s' and doesn't allow a null value." % (previous_obj, attr))

            return []

        self.m2m_resources = []
        m2m_dehydrated = []

        # TODO: Also model-specific and leaky. Relies on there being a
        # ``Manager`` there.

        filter = Q(**{'status': STATUS_PUBLISHED})



        for field_name, values in bundle.request.GET.iterlists():

            field_name = field_name.replace('jobs__', '').replace('jobs_', '')

            field_name = field_name.replace('skill_set', 'skills__icontains')

            if field_name in preserve_keys or field_name in ['has_jobs']:
                continue

            group_filter = None
            for value in values:
                if not group_filter:
                    group_filter = Q(**{field_name: value})
                else:
                    group_filter |= Q(**{field_name: value})

            filter &= group_filter


        for m2m in the_m2ms.filter(filter):
            m2m_resource = self.get_related_resource(m2m)
            m2m_bundle = Bundle(obj=m2m, request=bundle.request)
            self.m2m_resources.append(m2m_resource)
            m2m_dehydrated.append(self.dehydrate_related(m2m_bundle, m2m_resource, for_list=for_list))

        return m2m_dehydrated

# -- Relation Choices --
# http://localhost:8000/api/v1/organization_jobs/?jobs__country__permalink=hong-kong

# -- Range --
# http://localhost:8000/api/v1/organization_jobs/?jobs__equity_min__gte=5&jobs__equity_max__lte=5
# http://localhost:8000/api/v1/organization_jobs/?jobs__salary_min__gte=1000&jobs__salary_max__lte=1000
# http://localhost:8000/api/v1/organization_jobs/?jobs__years_of_experience__gte=3

# -- Tags --
# http://localhost:8000/api/v1/organization_jobs/?jobs__skills__icontains=php&jobs__skills__icontains=node.js

# Get Choices from job schema for Basic filter
# http://localhost:8000/api/v1/job/schema/

# -- Choices --
# http://localhost:8000/api/v1/organization_jobs/?jobs__role=software-engineer
# http://localhost:8000/api/v1/organization_jobs/?jobs__position=contract

# -- Boolean --
# http://localhost:8000/api/v1/organization_jobs/?jobs__remote=true

# -- String --
# http://localhost:8000/api/v1/organization_jobs/?jobs__title__icontains=nisl

# -- Suggestion --
# http://localhost:8000/api/v1/job/search/?q=health+technologies+php+javascript
# suggest by search and field are job.skills and organization.topics
# reverse are user.skills and user.topics


class JobResource(BaseResource):

    organization_jobs = fields.ToManyField('api.resources.OrganizationResource', 'organization_jobs', null=True, blank=True, full=True, full_detail=True, full_list=False, related_name='organization_jobs')
    country = fields.ForeignKey('api.resources.CountryResource', 'country',
                                related_name='country', null=True, blank=True,
                                full=True)
    skill_set = fields.ManyToManyField('api.resources.SkillResource', 'skill_set', related_name='skill_set',
                                       null=True, blank=True, full=True)

    get_position_display = fields.CharField(attribute='get_position_display', readonly=True)
    get_role_display = fields.CharField(attribute='get_role_display', readonly=True)

    class Meta:
        allowed_methods = ['get']
        queryset = Job.objects.filter(status=STATUS_PUBLISHED).order_by('-ordering').distinct()
        resource_name = 'job'
        include_absolute_url = True
        filtering = {
            'ordering': ALL,
            'organization_jobs': ALL_WITH_RELATIONS,
            'country': ALL_WITH_RELATIONS,
            'skills': ALL,
            'skill_set': ALL_WITH_RELATIONS,
            'role': ALL,
            'position': ALL,
            'salary_min': ALL,
            'salary_max': ALL,
            'equity_min': ALL,
            'equity_max': ALL,
            'remote': ALL,
            'years_of_experience': ALL,
            'title': ALL,
        }
        ordering = ['ordering', 'id', 'priority']
        excludes = ['is_deleted']


    def obj_get_list(self, bundle, **kwargs):

        for field_name, value in bundle.request.GET.items():
            if 'jobs__' in field_name:
                kwargs[field_name.replace('jobs__', '')] = value

        result = super(JobResource, self).obj_get_list(bundle, **kwargs)

        return result


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),

        ]

    def get_search(self, request, **kwargs):
        return base_get_search(self, request, Job, for_list=False, **kwargs)

class OrganizationJobsResource(BaseResource):


    ordering = fields.IntegerField(attribute='ordering')

    country = fields.ForeignKey('api.resources.CountryResource', 'country',
                                related_name='country', null=True, blank=True,
                                full=True, use_in='detail')

    get_thumbnail = fields.CharField(attribute='get_thumbnail')
    get_thumbnail_in_primary = fields.CharField(attribute='get_thumbnail_in_primary')
    get_display_name = fields.CharField(attribute='get_display_name')

    jobs = JobToManyFieldForList('api.resources.JobResource', 'jobs', null=True, blank=True, full=True)

    status = fields.IntegerField(attribute='status')

    class Meta:
        allowed_methods = ['get']
        authorization = UserAuthorization()
        detail_uri_name = 'permalink'
        queryset = Organization.objects.filter(jobs__isnull=False, status=STATUS_PUBLISHED, jobs__status=STATUS_PUBLISHED).order_by('-ordering').distinct()
        resource_name = 'organization_jobs'
        include_absolute_url = True

        fields = ['ordering', 'country', 'get_thumbnail', 'get_thumbnail_in_primary', 'jobs']

        filtering = {
            'ordering': ALL,
            'jobs': ALL_WITH_RELATIONS,
            'country': ALL_WITH_RELATIONS,
        }
        ordering = ['ordering', 'id', 'priority']


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        return base_get_search(self, request, Organization)


class UserExperienceOrganizationResource(BaseRelationResource):
    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True,
                            related_name='experience_src')
    dst = fields.ForeignKey('api.resources.PartyResource', 'dst', blank=True, full=True,
                            related_name='experience_dst')

    get_summary = fields.CharField(attribute='get_summary')

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = UserExperienceOrganization.objects.all().order_by('-end_date', '-start_date', '-created', 'id')
        resource_name = 'user_experience_organization'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst': ALL_WITH_RELATIONS,
            'id': ALL,
            'status': ALL,
        }
        ordering = ['id', 'end_date', 'status']


class CmsResource(BaseResource):
    get_thumbnail = fields.CharField(attribute='get_thumbnail')
    get_thumbnail_in_primary = fields.CharField(attribute='get_thumbnail_in_primary')
    get_summary = fields.CharField(attribute='get_summary')
    description = fields.CharField(attribute='description', null=True, blank=True, use_in='detail')
    topics = fields.ToManyField('api.resources.TopicItemResource', 'topics', related_name='topics',null=True, blank=True, full=True)


    class Meta:
        allowed_methods = ['get']
        queryset = CommonCms.objects.all().order_by('-created')
        fields = ['id', 'title', 'get_display_name', 'get_thumbnail','description', 'created']
        paginator_class = Paginator
        include_absolute_url = True
        filtering = {
            'id': ALL,
            'permalink': ALL,
            'topics': ALL_WITH_RELATIONS,
        }
        ordering = ['created', 'id']

class NewsResource(CmsResource):
    get_thumbnail = fields.CharField(attribute='get_thumbnail')
    get_thumbnail_in_primary = fields.CharField(attribute='get_thumbnail_in_primary')
    get_summary = fields.CharField(attribute='get_summary')
    description = fields.CharField(attribute='description', null=True, blank=True, use_in='detail')
    topics = fields.ToManyField('api.resources.TopicItemResource', 'topics', related_name='topics',null=True, blank=True, full=True)
    categories = fields.ToManyField('api.resources.ArticleCategoryItemResource', 'categories', related_name='categories',null=True, blank=True, full=True)
    cms_has_party_src = fields.ToManyField('api.resources.CmsHasPartyResource', 'cms_has_party_src', related_name='cms_has_party_src',null=True, blank=True, full=True)
    tag_set = fields.ToManyField('api.resources.TagResource', 'tag_set', related_name='tag_set',
                                 null=True, blank=True, full=True)
    get_files = fields.ListField(attribute='get_files' ,null=True, blank=True, use_in='detail')

    class Meta:
        allowed_methods = ['get']
        queryset = News.objects.all().order_by('-created')
        fields = ['id', 'title', 'get_display_name', 'get_thumbnail', 'description', 'created', 'article_category', 'homepage_url', 'get_files']
        paginator_class = Paginator
        include_absolute_url = True
        filtering = {
            'id': ALL,
            'permalink': ALL,
            'topics': ALL_WITH_RELATIONS,
            'categories': ALL_WITH_RELATIONS,
            'article_category': ALL,
            'teg_set': ALL_WITH_RELATIONS
        }
        ordering = ['created', 'id']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        return base_get_search(self, request, News)



class EventResource(CmsResource):
    get_thumbnail = fields.CharField(attribute='get_thumbnail')
    get_thumbnail_in_primary = fields.CharField(attribute='get_thumbnail_in_primary')
    get_summary = fields.CharField(attribute='get_summary')
    description = fields.CharField(attribute='description', null=True, blank=True, use_in='detail')
    topics = fields.ToManyField('api.resources.TopicItemResource', 'topics', related_name='topics',null=True, blank=True, full=True)
    cms_has_party_src = fields.ToManyField('api.resources.CmsHasPartyResource', 'cms_has_party_src', related_name='cms_has_party_src',null=True, blank=True, full=True)

    start_date = fields.DateField(attribute='start_date', null=True, blank=True)
    end_date = fields.DateField(attribute='end_date', null=True, blank=True)

    get_phones = fields.ListField(attribute='get_phones', null=True, blank=True, use_in='detail')

    class Meta:
        allowed_methods = ['get']
        queryset = Event.objects.all().order_by('start_date', 'created')

        fields = [
            'id', 'title', 'get_display_name', 'get_thumbnail','description',
            'created', 'start_date', 'end_date', 'time', 'location', 'phone',
            'email', 'facebook_url', 'twitter_url', 'homepage_url'
        ]
        paginator_class = Paginator
        include_absolute_url = True
        filtering = {
            'id': ALL,
            'permalink': ALL,
            'topics': ALL_WITH_RELATIONS,
            'start_date': ALL,
            'end_date': ALL,
        }
        ordering = ['start_date', 'end_date', 'created']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/summary/$" % (self._meta.resource_name),
                self.wrap_view('get_summary'), name="api_get_summary"),
        ]

    def get_summary(self, request, **kwargs):

        midnight = datetime.time(0)
        today = datetime.datetime.combine(timezone.now(), midnight)

        event_list = Event.objects.filter(end_date__gte=today, start_date__lte=today+timedelta(days=365))

        has_event_list = set()
        for event in event_list:
            has_event_list |= set(rrule.rrule(rrule.DAILY, count=(event.end_date-event.start_date).days+1, dtstart=event.start_date))

        has_event_list = [has_event.strftime("%Y-%m-%d") for has_event in has_event_list]

        return self.create_response(request, dict.fromkeys(has_event_list, 1))

class VerbResource(BaseResource):

    permalink = fields.IntegerField(attribute='id')

    class Meta:
        queryset = ContentType.objects.filter(app_label='relation')
        allowed_methods = ['get']
        resource_name = 'verb'
        filtering = {
            'name': ALL,
            'model': ALL,
            'app_label': ALL
        }

    def dehydrate(self, bundle):
        bundle = super(VerbResource, self).dehydrate(bundle)

        ModelClass = bundle.obj.model_class()

        bundle.data['title'] = (hasattr(ModelClass, 'REQUEST_VERB_DISPLAY') and ModelClass.REQUEST_VERB_DISPLAY) or bundle.data['name']
        bundle.data['swap'] = (hasattr(ModelClass, 'REQUEST_VERB_SWAP_DISPLAY') and ModelClass.REQUEST_VERB_SWAP_DISPLAY)

        bundle.data['swap'] = bool(bundle.data['swap'])
        if bundle.data['swap']:

            bundle.data['title_swap'] = (hasattr(ModelClass, 'REQUEST_VERB_SWAP_DISPLAY') and ModelClass.REQUEST_VERB_SWAP_DISPLAY) or bundle.data['name']
            bundle.data['title'] = '%s/%s' % (bundle.data['title'], bundle.data['title_swap'])

        return bundle


class PartyFollowingResource(PartyResource):
    organization = fields.ToOneField('api.resources.OrganizationResource', 'organization', related_name='organization', null=True, blank=True)
    user = fields.ToOneField('api.resources.UserResource', 'user', related_name='user', null=True, blank=True)


    class Meta:
        allowed_methods = ['get']
        queryset = Party.objects.filter((Q(organization__isnull=False) & Q(Q(organization__status=STATUS_PUBLISHED))) | (Q(user__isnull=False) & Q(user__is_active=True)))
        resource_name = 'party_following'
        include_absolute_url = True

        excludes = ['store_total_follower', 'store_total_following', 'store_total_love', 'store_total_testify']

        filtering = {
            'id': ALL,
            'organization': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS,

        }

    def get_object_list(self, request):
        query = super(PartyFollowingResource, self).get_object_list(request)


        focus_verbs = [
            ContentType.objects.get_for_model(OrganizationHasPeople),
            ContentType.objects.get_for_model(PartyPartnerParty),
            ContentType.objects.get_for_model(PartySupportParty),
            ContentType.objects.get_for_model(PartyInvestParty),
            ContentType.objects.get_for_model(PartyTestifyParty),
            ContentType.objects.get_for_model(UserExperienceOrganization),
            ContentType.objects.get_for_model(PartyReceivedFundingParty),
            ContentType.objects.get_for_model(PartyReceivedInvestingParty),
            ContentType.objects.get_for_model(Party.portfolios.through),
            ContentType.objects.get_for_model(Organization.jobs.through),

        ]
        query = query.filter(follow_dst__src__id=request.logged_in_party.id, follow_dst__status=STATUS_PUBLISHED) \
            .distinct() \
            .filter(Q(notification_receiver__verb__in=focus_verbs) | Q(notification_actor__verb__in=focus_verbs)) \
            .annotate(latest_receiver=Max('notification_receiver__created'), latest_actor=Max('notification_actor__created')) \
            .order_by('-latest_actor')
            # TODO: GREATEST(latest_receiver, latest_actor) is better

        roles = request.GET.get('roles')
        if roles is not None:
            query = query.filter(Q(organization__organization_roles=roles) | Q(user__user_roles=roles))

        return query


    def _build_reverse_url(self, name, args=None, kwargs=None):

        kwargs['resource_name'] = 'party'
        return reverse(name, args=args, kwargs=kwargs)


class HappeningResource(BaseResource):

    receiver = fields.ForeignKey('api.resources.PartyResource', 'receiver', full=True, full_detail=True, full_list=False)
    actor = fields.ForeignKey('api.resources.PartyResource', 'actor', full=True)
    verb = fields.ForeignKey('api.resources.VerbResource', 'verb', full=True)

    total_love = fields.IntegerField(attribute='total_love', null=True, blank=True)

    get_simple_html_display = fields.CharField(attribute='get_simple_html_display')

    approval_status = fields.IntegerField(attribute='approval_status', null=True, blank=True)

    REQUIRED_APPROVAL = fields.BooleanField(attribute='REQUIRED_APPROVAL')


    class Meta:
        queryset = Notification.objects\
            .filter(is_system=True, verb__isnull=False).exclude(status=STATUS_REJECTED)\
            .prefetch_related('receiver', 'actor', 'verb').order_by('-created')


        allowed_methods = ['get']
        resource_name = 'happening'
        filtering = {
            'receiver': ALL_WITH_RELATIONS,
            'actor': ALL_WITH_RELATIONS,
            'verb': ALL_WITH_RELATIONS
        }


    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)

        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()


        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for_list = True
        if request.GET.get('following'):
            for_list = False


        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=for_list))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        response = self.create_response(request, to_be_serialized)

        return response


    def get_object_list(self, request):
        query = super(HappeningResource, self).get_object_list(request)

        receiver_or_actor = request.GET.get('receiver_or_actor')
        if receiver_or_actor:
            query = query.filter(Q(receiver__id=receiver_or_actor) | Q(actor__id=receiver_or_actor))

        receiver_or_actor__role_permalink = request.GET.get('receiver_or_actor__role_permalink')
        if receiver_or_actor__role_permalink:
            query = query.filter(
                Q(receiver__organization__organization_roles__permalink=receiver_or_actor__role_permalink) |
                Q(actor__organization__organization_roles__permalink=receiver_or_actor__role_permalink)
            ).distinct()

        receiver_or_actor__is_user = request.GET.get('receiver_or_actor__is_user')
        if receiver_or_actor__is_user:
            query = query.filter(
                Q(receiver__user__isnull=False) |
                Q(actor__user__isnull=False)
            ).distinct()

        following = request.GET.get('following')
        if following:
            focus_verbs = [
                ContentType.objects.get_for_model(OrganizationHasPeople),
                ContentType.objects.get_for_model(PartyPartnerParty),
                ContentType.objects.get_for_model(PartySupportParty),
                ContentType.objects.get_for_model(PartyInvestParty),
                ContentType.objects.get_for_model(PartyTestifyParty),
                ContentType.objects.get_for_model(UserExperienceOrganization),
                ContentType.objects.get_for_model(PartyReceivedFundingParty),
                ContentType.objects.get_for_model(PartyReceivedInvestingParty),

            ]
            query = query.filter(Q(receiver__follow_dst__src__id=request.logged_in_party.id) | Q(actor__follow_dst__src__id=request.logged_in_party.id))\
                         .filter(verb__in=focus_verbs)\
                         .order_by('-created').distinct()

        unpublished = request.GET.get('unpublished')
        if not unpublished and not settings.DISPLAY_UNPUBLISHED_HAPPENING:
            query = query.filter(
                            (Q(actor__organization__isnull=False) & Q(actor__organization__status=STATUS_PUBLISHED)) |
                            (Q(actor__user__isnull=False) & Q(actor__user__is_active=True))

                        ).filter(
                            (Q(receiver__organization__isnull=False) & Q(receiver__organization__status=STATUS_PUBLISHED)) |
                            (Q(receiver__user__isnull=False) & Q(receiver__user__is_active=True))
                        )

        if request.GET.get('actor_unique'):
            items = query.values('actor').annotate(first_actor=Count('actor'), max_id=Max('id'), max_created=Max('created')).order_by('-max_id').values_list('max_id', flat=True)

            #items = items[0:request.GET.get('limit') or 20]

            #ids = [item[0] for item in items]
            query = Notification.objects.filter(id__in=items).order_by('-created')


        return query


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/summary/$" % (self._meta.resource_name),
                self.wrap_view('get_summary'), name="api_get_summary"),
        ]

    def get_summary(self, request, **kwargs):

        summary = get_summary()
        return self.create_response(request, summary)

    def dehydrate(self, bundle):

        bundle = super(HappeningResource, self).dehydrate(bundle)

        bundle.data['is_love'] = False
        bundle.data['can_love'] = False

        if bundle.request.user.is_authenticated():
            bundle.data['can_love'] = True
            bundle.data['is_love'] = bundle.obj.is_love(bundle.request.logged_in_party)

        return bundle


class PageNumberPaginator(Paginator):
    def get_offset(self):
        page = int(self.request_data.get('page', 1))
        if page:
            #self.request_data['offset'] = (page-1)*self.get_limit()
            return (page-1)*self.get_limit()

        return  super(PageNumberPaginator, self).get_offset()



class SearchResource(Resource):

    id = fields.IntegerField(attribute='id', readonly=True, null=True)
    get_thumbnail = fields.CharField(attribute='get_thumbnail', readonly=True, null=True)
    get_thumbnail_in_primary = fields.CharField(attribute='get_thumbnail_in_primary', readonly=True, null=True)
    get_display_name = fields.CharField(attribute='get_display_name', readonly=True, null=True)
    get_summary = fields.CharField(attribute='get_summary', readonly=True, null=True)


    inst_type = fields.CharField(attribute='inst_type', readonly=True, null=True)
    get_class_display = fields.CharField(attribute='get_class_display', readonly=True, null=True)

    permalink = fields.CharField(attribute='permalink', readonly=True, null=True)
    absolute_url = fields.CharField(attribute='get_absolute_url', readonly=True, null=True)

    class Meta:
        resource_name = 'search'
        authorization = Authorization()
        paginator_class = PageNumberPaginator

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):

        results = base_get_search(self, request, get_queryset=True)
        return results

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def cast(self, search_obj):

        obj_dict = {'id': search_obj.pk}

        for field in search_obj.model._meta.fields:

            if field.name in ['pk', 'id']:
                continue

            if type(field) is models.ForeignKey:

                value = getattr(search_obj, field.name)
                if value:
                    obj_dict[field.name] = field.rel.to(permalink=value)

            else:
                value = getattr(search_obj, field.name)
                if value:
                    obj_dict[field.name] = value

        inst = search_obj.model(**obj_dict)

        for field in search_obj.model._meta.many_to_many:

            values = getattr(search_obj, field.name) or []
            setattr(inst, '_%s' % field.name, [field.rel.to(permalink=value) for value in values])

        return inst

    def full_dehydrate(self, bundle, for_list=False):
        bundle.obj = self.cast(bundle.obj)
        super(SearchResource, self).full_dehydrate(bundle, for_list=False)
        return bundle

    def dehydrate_resource_uri(self, bundle):
        return super(SearchResource, self).dehydrate_resource_uri(bundle)
    

# Take action
class PartyLoveResource(BasePartySendUniqueDataPartyResource):

    src = fields.ForeignKey('api.resources.PartyResource', 'src', blank=True, full=True)
    dst_content_type = fields.ForeignKey('api.resources.ContentTypeResource', 'dst_content_type', blank=True, full=True)
    dst = GenericForeignKeyField({
        Party: PartyResource,
        Notification: HappeningResource,
    }, 'dst', null=True, blank=True, full=True)

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = PartyLove.objects.filter(status=STATUS_PUBLISHED).order_by('-id')
        resource_name = 'party_love'
        filtering = {
            'src': ALL_WITH_RELATIONS,
            'dst_content_type': ALL_WITH_RELATIONS,
            'dst_id': ALL,
            'status': ALL,
        }

        ordering = ['id']



class NotificationResource(BaseResource):
    receiver = fields.ForeignKey('api.resources.PartyResource', 'receiver')
    actor = fields.ForeignKey('api.resources.PartyResource', 'actor', full=True)
    verb = fields.ForeignKey('api.resources.VerbResource', 'verb', blank=True)

    organization = fields.ForeignKey('api.resources.PartyResource', 'organization', full=True, null=True, blank=True)

    approval_status = fields.IntegerField(attribute='approval_status', null=True, blank=True)

    get_html_display = fields.CharField(attribute='get_html_display')


    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = Notification.objects.filter(is_system=None, verb__isnull=False).prefetch_related('receiver', 'actor', 'verb', 'organization', 'target').order_by('-created')
        resource_name = 'notification'
        filtering = {
            'receiver': ALL_WITH_RELATIONS,
            'actor': ALL_WITH_RELATIONS,
            'verb': ALL_WITH_RELATIONS,
            'target_id': ALL,
            'status': ALL,
            'id': ALL,
            'is_system': ALL
        }

        ordering = ['id', 'status']


    def dehydrate(self, bundle):

        bundle = super(NotificationResource, self).dehydrate(bundle)
        bundle.data['approval_required'] = bundle.obj.approval_required(bundle.request)


        if bundle.data['approval_required'] and bundle.obj.verb:


            TargetResource = {
                OrganizationHasPeople: OrganizationHasPeopleResource,
                PartyPartnerParty: PartyPartnerPartyResource,
                PartySupportParty: PartySupportPartyResource,
                PartyInvestParty: PartyInvestPartyResource,
                PartyFollowParty: PartyFollowPartyResource,
                PartyReceivedFundingParty: PartyReceivedFundingPartyResource,
                PartyReceivedInvestingParty: PartyReceivedInvestingPartyResource,
                PartyTestifyParty: PartyTestifyPartyResource,
                PartyInviteTestifyParty: PartyInviteTestifyPartyResource,
                UserExperienceOrganization: UserExperienceOrganizationResource,
                PartyLove: PartyLoveResource,

            }[bundle.obj.verb.model_class()]

            target_resource = TargetResource()

            bundle.data['target'] = target_resource.get_resource_uri(bundle.obj.target)

        return bundle


    def get_list(self, request, **kwargs):

        base_bundle = self.build_bundle(request=request)

        kwargs['receiver'] = request.logged_in_party.id

        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()


        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

            # Mask all read
            obj.status = Notification.STATUS_READ
            obj.save()


        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        response = self.create_response(request, to_be_serialized)


        return response

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/new_count/$" % (self._meta.resource_name),
                self.wrap_view('get_new_count'), name="api_get_new_count"),
        ]

    def get_new_count(self, request, **kwargs):

        new_count = Notification.objects.filter(
            status=Notification.STATUS_NEW,
            receiver__id=request.logged_in_party.id,
            is_system=None
        ).count()

        return self.create_response(request, new_count)


class RequestResource(NotificationResource):

    get_html_display = fields.CharField(attribute='get_request_html_display')

    class Meta:
        serializer = VerboseSerializer(formats=['json'])
        authorization = UserAuthorization()
        always_return_data = True
        queryset = Notification.objects.filter(is_system=None, party__isnull=True, organization__isnull=True)\
            .prefetch_related('receiver', 'actor', 'verb', 'organization', 'target')\
            .order_by('-created')

        resource_name = 'request'
        filtering = {
            'receiver': ALL_WITH_RELATIONS,
            'actor': ALL_WITH_RELATIONS,
            'verb': ALL_WITH_RELATIONS,
            'target_id': ALL,
            'status': ALL,
            'id': ALL,
            'is_system': ALL,
        }

        ordering = ['id', 'status']

    def _build_reverse_url(self, name, args=None, kwargs=None):
        kwargs['resource_name'] = 'notification'
        return reverse(name, args=args, kwargs=kwargs)


    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)

        kwargs['actor'] = request.logged_in_party.id

        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()


        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

            # Mask all read
            obj.status = Notification.STATUS_READ
            obj.save()

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        response = self.create_response(request, to_be_serialized)

        return response
