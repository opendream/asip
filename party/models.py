from decimal import Decimal
from django.apps import apps
from django.db.models import Sum
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from common.constants import STATUS_PUBLISHED
from common.functions import instance_get_thumbnail
from common.models import CommonTrashModel, CommonModel, PriorityModel, CachedModel, StatisitcAccess
import files_widget
from relation.models import PartyFollowParty, PartyTestifyParty, PartyLove
from special.models import Special
from taxonomy.models import Country

USER_MODEL = settings.AUTH_USER_MODEL

class Party(CommonTrashModel, CommonModel, CachedModel):

    country = models.ForeignKey('taxonomy.Country', null=True, blank=True, related_name='country', default=settings.DEFAULT_COUNTRY)
    portfolios = models.ManyToManyField('party.Portfolio', related_name='party_portfolios', null=True, blank=True)

    promote = models.NullBooleanField()

    # Denormalize
    store_total_follower = models.PositiveIntegerField(null=True, blank=True)
    store_total_following = models.PositiveIntegerField(null=True, blank=True)
    store_total_love = models.PositiveIntegerField(null=True, blank=True)
    store_total_testify = models.PositiveIntegerField(null=True, blank=True)

    store_popular = models.DecimalField(max_digits=19, decimal_places=8, null=True, blank=True)

    specials = models.ManyToManyField(Special, related_name='specials_party_list', null=True, blank=True)

    inst_type = None
    inst = None

    CREATED_ON_PUBLISHED = True

    NOTIFICATION_CHECK_CRAZY_CREATED = False
    NOTIFICATION_VERB_DISPLAY = _('%s joins the network')
    NOTIFICATION_VERB_DISPLAY_EMAIL = _('%s has been published')

    def get_inst(self):

        if self.inst:
            return self.inst

        if self.id and not hasattr(self, 'party_ptr'):
            try:
                self.inst = self.user
                self.inst_type = 'user'
            except:

                self.inst = self.organization
                self.inst_type = 'organization'

            return self.inst

        return self

    def get_deep_inst(self):

        if self.id and not hasattr(self, 'party_ptr'):
            try:
                self.inst = self.user
                self.inst_type = 'user'
            except:

                try:
                    self.inst = self.organization.program
                    self.inst_type = 'program'
                except:
                    self.inst = self.organization
                    self.inst_type = 'organization'

            return self.inst

        return self

    def get_inst_type(self):

        if self.inst_type:
            return self.inst_type

        self.get_inst()
        return self.inst_type

    def get_thumbnail(self):
        inst = self.get_inst()
        return inst and inst.get_thumbnail()

    def get_thumbnail_in_primary(self):
        inst = self.get_inst()
        return inst and inst.get_thumbnail_in_primary()

    def get_display_name(self):
        inst = self.get_inst()
        return inst and inst.get_display_name()

    def get_short_name(self):
        inst = self.get_inst()
        return inst and inst.get_short_name()

    def get_summary(self):
        inst = self.get_inst()
        return inst and inst.get_summary()

    def get_absolute_url(self):
        inst = self.get_inst()
        return inst and inst.get_absolute_url()

    def _ordering(self):
        inst = self.get_inst()
        return inst and inst.ordering

    def get_status(self):
        inst = self.get_inst()
        return inst and ((hasattr(inst, 'status') and inst.status) or (hasattr(inst, 'is_active') and inst.is_active))

    def is_program(self):
        inst = self.get_inst()
        return inst and hasattr(inst, 'program')

    def is_following(self, logged_in_party):
        return bool(self.follow_dst.filter(src=logged_in_party, status=STATUS_PUBLISHED).distinct().count())

    def is_love(self, logged_in_party):
        return bool(PartyLove.objects.filter(
            src=logged_in_party,
            dst_content_type=ContentType.objects.get_for_model(self.__class__),
            dst_id=self.id,
            status=STATUS_PUBLISHED
        ).count())

    def build_total(self, field_names=[], not_save=False):

        if not self.id:
            return False

        content_type = ContentType.objects.get_for_model(self.get_deep_inst().__class__)

        if not field_names or ('total_follower' in field_names):
            self.store_total_follower = PartyFollowParty.objects.filter(dst=self, status=STATUS_PUBLISHED).count()

        if not field_names or ('total_following' in field_names):
            self.store_total_following = PartyFollowParty.objects.filter(src=self, status=STATUS_PUBLISHED).count()

        if not field_names or ('total_love' in field_names):
            self.store_total_love = PartyLove.objects.filter(
                dst_content_type=content_type,
                dst_id=self.id,
                status=STATUS_PUBLISHED).count()
            print 'self.store_total_love', content_type, self.store_total_love

        if not field_names or ('total_testify' in field_names):
            self.store_total_testify = PartyTestifyParty.objects.filter(dst=self, status=STATUS_PUBLISHED).count()

        if not field_names or ('popular' in field_names):
            views_point = StatisitcAccess.objects.filter(
                object_id=self.id
            ).aggregate(Sum('id'))['id__sum'] or 0

            love_point = PartyLove.objects.filter(
                dst_content_type=content_type,
                dst_id=self.id,
                status=STATUS_PUBLISHED
            ).aggregate(Sum('id'))['id__sum'] or 0

            follower_point = PartyFollowParty.objects.filter(
                dst=self, status=STATUS_PUBLISHED
            ).aggregate(Sum('id'))['id__sum'] or 0

            testify_point = PartyTestifyParty.objects.filter(
                dst=self, status=STATUS_PUBLISHED
            ).aggregate(Sum('id'))['id__sum'] or 0

            point = (1*views_point) + (20*love_point) + (30*follower_point) + (100*testify_point)

            if hasattr(self, 'priority'):
                point += (Decimal(100000000) * Decimal(self.priority))


            point += Decimal(self.id)*Decimal(1)/Decimal(100000000)


            self.store_popular = point

        if not not_save:
            self.save()

    # Use for developer
    def clear_total(self):

        self.store_total_follower = None
        self.store_total_following = None
        self.store_total_love = None
        self.store_total_testify = None
        self.store_popular = None
        self.save()

    @property
    def total_follower(self):
        if self.store_total_follower is None:
            self.build_total()

        return self.store_total_follower

    @property
    def total_following(self):
        if self.store_total_following is None:
            self.build_total()
        return self.store_total_following

    @property
    def total_love(self):
        if self.store_total_love is None:
            self.build_total()
        return self.store_total_love

    @property
    def total_testify(self):
        if self.store_total_testify is None:
            self.build_total()
        return self.store_total_testify

    @property
    def popular(self):
        if self.store_popular is None:
            self.build_total()
        return self.store_popular


    def __unicode__(self):
        return self.get_display_name()


class Portfolio(CommonModel, PriorityModel):

    title = models.CharField(max_length=255)
    images = files_widget.ImagesField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '%s##portfolio-%s' % (self.party_portfolios.all()[0].get_absolute_url(), self.id)

    def get_thumbnails(self):
        return instance_get_thumbnail(self, field_name='images', size='306x190', crop='center', upscale=True)

    def get_images(self):
        return instance_get_thumbnail(self, field_name='images', size='345', crop=None, upscale=False)

    def __unicode__(self):
        return self.title