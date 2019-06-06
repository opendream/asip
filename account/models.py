import re
import tagging

from ckeditor.fields import RichTextField
from django.core import validators
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db.models import Q
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from common.constants import SUMMARY_MAX_LENGTH
from common.functions import instance_get_thumbnail
from common.models import PriorityModel, CommonTrashModel
import files_widget

from django.conf import settings
from organization.models import Organization, USER_MODEL
from party.models import Party
from relation.models import PartyContactParty, PartyTestifyParty, PartyLove
from tagging_autocomplete_tagit.models import TagAutocompleteTagItField


class AbstractPeopleField(models.Model):
    image = files_widget.ImageField(null=True, blank=True)

    # Internal
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    occupation = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    # Taxonomy
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True)
    interests = models.ManyToManyField('taxonomy.Topic', null=True, blank=True, related_name='interests')
    user_roles = models.ManyToManyField('taxonomy.UserRole', null=True, blank=True, related_name='user_roles')
    skills = TagAutocompleteTagItField(max_tags=False, null=True, blank=True)

    # External
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    homepage_url = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def permalink(self):
        return self.username

    @permalink.setter
    def permalink(self, value):
        self.username = value

    def get_thumbnail(self):
        return instance_get_thumbnail(self, 'image')

    def get_thumbnail_in_primary(self):
        return instance_get_thumbnail(self, size='150x150', crop='center', upscale=True)

    def get_full_name(self):
        try:
            full_name = '%s %s' % (self.first_name or '', self.last_name or '')
            return full_name.strip()
        except:
            return ''

    def get_short_name(self):
        output = ''
        try:
            if self.first_name.strip() and self.last_name.strip():
                output = '%s.%s' % (self.first_name.strip(), self.last_name.strip()[0])

            elif self.first_name.strip():
                output = self.first_name.strip()

            elif self.last_name.strip():
                output = self.last_name.strip()

            output = ''
        except:
            output = ''

        if not output:
            output = self.username

        return output

    def get_display_name(self, allow_email=False):
        if allow_email:
            return self.get_full_name() or self.email or self.username

        return self.get_full_name() or self.username

    def get_summary(self):
        summary = self.summary or self.occupation or ''
        return truncatechars(summary, SUMMARY_MAX_LENGTH)

    def __unicode__(self):
        return self.get_full_name() or self.username or self.email



class User(AbstractPeopleField, Party, AbstractBaseUser, PermissionsMixin, PriorityModel):

    inst_type = 'user'

    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])

    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    # User relation
    notification_allow_email_send_organizationhaspeople = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_partysupportparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_partyfollowparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_partycontactparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_partytestifyparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_partylove = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_partyinvitetestifyparty = models.NullBooleanField(null=True, blank=True, default=True)


    # Organization relation
    notification_allow_email_send_organization_partypartnerparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_userexperienceorganization = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_partysupportparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_partyfollowparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_partycontactparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_partytestifyparty = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_partylove = models.NullBooleanField(null=True, blank=True, default=True)
    notification_allow_email_send_organization_partyinvitetestifyparty = models.NullBooleanField(null=True, blank=True, default=True)

    # Follow party
    notification_allow_email_send_from_follow = models.NullBooleanField(null=True, blank=True, default=True)

    # Deprecated
    user_email_notification = models.NullBooleanField(null=True, blank=True)
    organization_email_notification = models.NullBooleanField(null=True, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    is_editor = models.BooleanField(_('editor status'), default=False)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Deprecated
    party_activated = models.ForeignKey('party.Party', related_name='party_activated', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_absolute_url(self):
        return reverse('people_detail', args=[self.username, self.id])

    @property
    def inst_name(self):
        return _('People')

    def can_edit(self, request, instance, bypass_created=False):


        if bypass_created and not self.id:
            return False

        editable = False

        if hasattr(instance, 'get_inst'):
            instance = instance.get_inst()

        if self.is_staff or \
           (hasattr(instance, 'username') and instance.id == self.id) or \
           (hasattr(instance, 'created_by') and self == instance.created_by) or \
           (hasattr(instance, 'src') and self.id == instance.src.id):

            editable = True

        if hasattr(instance, 'admins'):
            editable = editable or bool(instance.admins.filter(id=self.id).count())

        elif hasattr(instance, 'src') and instance.src.__class__ in [Party, Organization]:
            editable = editable or bool(self.admins.filter(id=instance.src.id).count())


        elif hasattr(instance, 'party_portfolios'):
            editable = editable or bool(instance.party_portfolios.all()[0].admins.filter(id=self.id).count())

        elif hasattr(instance, 'organization_jobs'):
            editable = editable or bool(instance.organization_jobs.all()[0].admins.filter(id=self.id).count())

        if instance.__class__ in [PartyContactParty, PartyTestifyParty]:
            # TODO: check only update status
            editable = editable or (instance.dst.id == request.logged_in_party.id) or (instance.src.id == request.logged_in_party.id)

        return editable

tagging.register(User, tag_descriptor_attr='skill_set')


class AppConnect(CommonTrashModel):

    created_by = models.ForeignKey(USER_MODEL, related_name='apps')

    app_id = models.CharField(max_length=255, verbose_name="App ID", null=True, blank=True)
    name = models.CharField(max_length=255)
    site_uri = models.CharField(max_length=512, verbose_name="Site URI", help_text="Exclude http or https, for development allow localhost")
    description = models.CharField(max_length=512, null=True, blank=True)
    image = files_widget.ImageField(null=True, blank=True, verbose_name="Logo")


    def get_absolute_url(self):
        return reverse('account_app_detail', args=[self.app_id])




