from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext as _

from common.constants import STATUS_CHOICES, STATUS_PENDING, SUMMARY_MAX_LENGTH, STATUS_PUBLISHED, STATUS_DELETED, STATUS_REJECTED
from common.models import PriorityModel, CommonModel, CachedModel


RELATION_STATUS_CHOICES = STATUS_CHOICES + ((STATUS_DELETED, 'Deleted'), )

class BaseRelation(CommonModel, PriorityModel, CachedModel):
    STATUS_PENDING = STATUS_PENDING
    STATUS_PUBLISHED = STATUS_PUBLISHED
    STATUS_DELETED = STATUS_DELETED
    STATUS_REJECTED = STATUS_REJECTED
    RELATION_STATUS_CHOICES = RELATION_STATUS_CHOICES

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    data = models.TextField(null=True, blank=True)

    origin = None

    NOTIFICATION_CHECK_CRAZY_CREATED = True
    NOTIFICATION_VERB_DISPLAY = _('Not implement %s')
    NOTIFICATION_PRIVATE = False

    REQUIRED_APPROVAL = True

    CROSS_TARGET = False

    class Meta:
        abstract = True


    def save(self, *args, **kwargs):

        if hasattr(self, 'src') and hasattr(self, 'dst'):

            src = self.src.party_ptr if hasattr(self.src, 'party_ptr') else self.src
            dst = self.dst.party_ptr if hasattr(self.dst, 'party_ptr') else self.dst
            if src == dst:
                raise PermissionDenied()

            super(BaseRelation, self).save(*args, **kwargs)

            if hasattr(self, 'rebuild_total_fields'):

                src = src.__class__.objects.get(id=src.id)
                dst = dst.__class__.objects.get(id=dst.id)
                src.build_total(field_names=self.rebuild_total_fields)
                dst.build_total(field_names=self.rebuild_total_fields)

        else:
            super(BaseRelation, self).save(*args, **kwargs)


        from notification.models import Notification

        if self.id:
            if self.status == STATUS_REJECTED:
                for notification in Notification.objects.filter(target_id=self.id, is_system=True):
                    notification.status = STATUS_REJECTED
                    notification.save()

            elif self.status == STATUS_PUBLISHED:
                for notification in Notification.objects.filter(target_id=self.id, is_system=True):
                    notification.status = STATUS_PUBLISHED
                    notification.save()


    def delete(self, *args, **kwargs):

        if hasattr(self, 'src') and hasattr(self, 'dst'):
            src = self.src.party_ptr if hasattr(self.src, 'party_ptr') else self.src
            dst = self.dst.party_ptr if hasattr(self.dst, 'party_ptr') else self.dst

            super(BaseRelation, self).delete(*args, **kwargs)

            if hasattr(self, 'rebuild_total_fields'):
                src = src.__class__.objects.get(id=src.id)
                dst = dst.__class__.objects.get(id=dst.id)
                src.build_total(field_names=self.rebuild_total_fields)
                dst.build_total(field_names=self.rebuild_total_fields)

        else:
            super(BaseRelation, self).save(*args, **kwargs)



class OrganizationHasPeople(BaseRelation):
    src = models.ForeignKey('organization.Organization', related_name='organization_has_people_src')
    dst = models.ForeignKey('account.User', related_name='organization_has_people_dst')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    NOTIFICATION_VERB_DISPLAY = _('adds %s as people in organization')
    REQUEST_VERB_DISPLAY = _('Add people to organization')

class PartyPartnerParty(BaseRelation):
    src = models.ForeignKey('party.Party', related_name='partner_src')
    dst = models.ForeignKey('party.Party', related_name='partner_dst')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    NOTIFICATION_VERB_DISPLAY = _('add %s as partner')
    CROSS_TARGET = True
    REQUEST_VERB_DISPLAY = 'Partner'


class PartySupportParty(BaseRelation):
    src = models.ForeignKey('party.Party', related_name='support_src')
    dst = models.ForeignKey('party.Party', related_name='support_dst')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    swap = models.NullBooleanField(null=True, blank=True)

    NOTIFICATION_VERB_DISPLAY = _('gives support to %s')
    NOTIFICATION_VERB_SWAP_DISPLAY = _('is supported by %s')
    REQUEST_VERB_DISPLAY = 'Give support'
    REQUEST_VERB_SWAP_DISPLAY = 'Supported by'


class PartyInvestParty(BaseRelation):
    src = models.ForeignKey('party.Party', related_name='invest_src')
    dst = models.ForeignKey('party.Party', related_name='invest_dst')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    swap = models.NullBooleanField(null=True, blank=True)

    NOTIFICATION_VERB_DISPLAY = _('invest in %s')
    NOTIFICATION_VERB_SWAP_DISPLAY = _('is invested by %s')

    REQUEST_VERB_DISPLAY = 'Invest to'
    REQUEST_VERB_SWAP_DISPLAY = 'Invested by'


# Has pagination not map m2m fields
class PartyFollowParty(BaseRelation):
    src = models.ForeignKey('party.Party', related_name='follow_src')
    dst = models.ForeignKey('party.Party', related_name='follow_dst')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PUBLISHED)

    rebuild_total_fields = ['total_following', 'total_follower', 'popular']

    NOTIFICATION_CHECK_CRAZY_CREATED = False
    NOTIFICATION_VERB_DISPLAY = _('is now following %s')
    REQUEST_VERB_DISPLAY = _('Follow')

    REQUIRED_APPROVAL = False


# Has pagination not map m2m fields
class PartyContactParty(BaseRelation):
    STATUS_UNREAD = 0
    STATUS_READ = 1
    READ_STATUS_CHOICES = (
        (STATUS_UNREAD, 'Unread'),
        (STATUS_READ, 'Read'),
    )

    src = models.ForeignKey('party.Party', related_name='contact_src')
    dst = models.ForeignKey('party.Party', related_name='contact_dst')

    status = models.IntegerField(choices=READ_STATUS_CHOICES, default=STATUS_UNREAD)

    system = models.NullBooleanField(null=True, blank=True)

    NOTIFICATION_CHECK_CRAZY_CREATED = False
    NOTIFICATION_VERB_DISPLAY = _('sends a message to %s')
    NOTIFICATION_DATA_DISPLAY = _('Active as this organization to see the message')
    NOTIFICATION_PRIVATE = True
    NOTIFICATION_VERB_SYSTEM_DISPLAY = _('request more financial information to %s')

    REQUIRED_APPROVAL = False
    REQUEST_VERB_DISPLAY = 'Message'

    def get_absolute_url(self):
        return '%s?next=%s' % (reverse('party_activate', args=[self.dst.id]), reverse('message_list'))


# Has pagination not map m2m fields
class PartyTestifyParty(BaseRelation):
    POINT_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    src = models.ForeignKey('party.Party', related_name='testify_src')
    dst = models.ForeignKey('party.Party', related_name='testify_dst')
    point = models.IntegerField(choices=POINT_CHOICES, default=0)

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    rebuild_total_fields = ['total_testify', 'popular']

    NOTIFICATION_CHECK_CRAZY_CREATED = False
    NOTIFICATION_VERB_DISPLAY = _('gives testimonial to %s')
    REQUEST_VERB_DISPLAY = _('Testimonial')


    def get_absolute_url(self):
        return '%s##testimonials' % self.dst.get_absolute_url()


class UserExperienceOrganization(BaseRelation):

    src = models.ForeignKey('account.User', blank=True, null=True, related_name='experience_src')
    dst = models.ForeignKey('organization.Organization', related_name='experience_dst')

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    NOTIFICATION_VERB_DISPLAY = _('now works at %s')
    REQUEST_VERB_DISPLAY = _('Experience')
    NOTIFICATION_DATE_FIELD = 'start_date'


    def get_summary(self):
        return truncatechars(self.description, SUMMARY_MAX_LENGTH)


class PartyReceivedFundingParty(BaseRelation):

    src = models.ForeignKey('party.Party', blank=True, null=True, related_name='received_funding_src')
    dst = models.ForeignKey('party.Party', blank=True, null=True, related_name='received_funding_dst')

    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
    )

    title = models.CharField(null=True, blank=True, max_length=255)

    date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    swap = models.NullBooleanField(null=True, blank=True)


    NOTIFICATION_VERB_DISPLAY = _('receives funding from %s')
    NOTIFICATION_VERB_SWAP_DISPLAY = _('gives funding to %s')
    NOTIFICATION_DATE_FIELD = 'date'

    NOTIFICATION_DATA_FIELD = 'amount'
    NOTIFICATION_DATA_FIELD_IS_INTEGER = True
    NOTIFICATION_DATA_SUFFIX = settings.CURRENCY
    REQUEST_VERB_DISPLAY = 'Receives Funding'
    REQUEST_VERB_SWAP_DISPLAY = 'Gives Funding'


    def get_absolute_url(self):
        return '%s##happening' % self.src.get_absolute_url()


class PartyReceivedInvestingParty(BaseRelation):

    src = models.ForeignKey('party.Party', blank=True, null=True, related_name='received_investing_src')
    dst = models.ForeignKey('party.Party', blank=True, null=True, related_name='received_investing_dst')

    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
    )

    title = models.CharField(null=True, blank=True, max_length=255)

    date = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)

    swap = models.NullBooleanField(null=True, blank=True)


    NOTIFICATION_VERB_DISPLAY = _('receives investment from %s')
    NOTIFICATION_VERB_SWAP_DISPLAY = _('invest to %s')
    NOTIFICATION_DATE_FIELD = 'date'

    NOTIFICATION_DATA_FIELD = 'amount'
    NOTIFICATION_DATA_FIELD_IS_INTEGER = True
    NOTIFICATION_DATA_SUFFIX = settings.CURRENCY
    REQUEST_VERB_DISPLAY = _('Receives Investing')
    REQUEST_VERB_SWAP_DISPLAY = _('Gives Investing')

    def get_absolute_url(self):
        return '%s##happening' % self.src.get_absolute_url()


class PartyInviteTestifyParty(BaseRelation):
    src = models.ForeignKey('party.Party', related_name='invite_testify_src')
    dst = models.ForeignKey('party.Party', related_name='invite_testify_dst')
    party = models.ForeignKey('party.Party', related_name='invite_testify_party')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PENDING)


    NOTIFICATION_VERB_DISPLAY = _('invites %s gives testimonial to %s')
    NOTIFICATION_DATA_FIELD = 'data'

    REQUIRED_APPROVAL = False
    REQUEST_VERB_DISPLAY = _('Invite testimonial')

    def get_absolute_url(self):
        return '%s##testimonials' % self.party.get_absolute_url()

    def __unicode__(self):
        return self.party.get_display_name()


class PartyLove(BaseRelation):

    src = models.ForeignKey('party.Party', related_name='love_src')

    dst_id = models.PositiveIntegerField()
    dst_content_type = models.ForeignKey(ContentType)
    dst = GenericForeignKey('dst_content_type', 'dst_id')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PUBLISHED)

    rebuild_total_fields = ['total_love', 'popular']

    NOTIFICATION_CHECK_CRAZY_CREATED = False
    NOTIFICATION_VERB_DISPLAY = _('loves %s')
    REQUEST_VERB_DISPLAY = _('Love')

    REQUIRED_APPROVAL = False


class CmsHasParty(BaseRelation):
    src = models.ForeignKey('cms.CommonCms', related_name='cms_has_party_src')
    dst = models.ForeignKey('party.Party', related_name='cms_has_party_dst')

    status = models.IntegerField(choices=RELATION_STATUS_CHOICES, default=STATUS_PUBLISHED)

    NOTIFICATION_VERB_DISPLAY = _('add %s in the news')
    NOTIFICATION_DATA_FIELD = 'src.title'
    NOTIFICATION_ACTOR_FIELD = 'party_created_by'
    NOTIFICATION_TARGET_FIELD = 'src'

    CROSS_TARGET = True
    REQUEST_VERB_DISPLAY = 'In The News'

    REQUIRED_APPROVAL = False
