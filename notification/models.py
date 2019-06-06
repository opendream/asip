# encoding=utf8
import sys
from celery.task import task
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
import requests

reload(sys)
sys.setdefaultencoding('utf8')

import re
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, send_mass_mail
from django.core.urlresolvers import reverse
#from django_asynchronous_send_mail import send_mail
from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
import sys
from django.template.defaultfilters import truncatechars
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import int_to_base36, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from account.functions import user_can_update_status, user_can_edit
from account.models import User
from asip.settings import DEFAULT_FROM_EMAIL, SITE_NAME
from common.constants import STATUS_DELETED, STATUS_PENDING, STATUS_PUBLISHED, STATUS_DRAFT
from common.signals import get_request
from organization.models import Organization
from party.models import Party
from relation.models import PartyContactParty, PartyFollowParty, PartyLove



# Config for notification
notification_app_includes = ['relation']
notification_model_excludes = [PartyContactParty]
notification_m2m_includes = [Organization.admins.through, Party.portfolios.through, Organization.jobs.through]
notification_m2m_private_includes = [Organization.admins.through]

notification_system_includes = [Organization, User]

notification_m2m_verb_display = {
    Organization.admins.through: 'adds %s as admin in organization',
    Party.portfolios.through: '<span style="display:none" class="happening-show">%s </span>create the new portfolio %s',
    Organization.jobs.through: '<span style="display:none" class="happening-show">%s </span>add a new job %s'
}


allow_create_notification = False
if 'loaddata' not in sys.argv:
    allow_create_notification = True


class Notification(models.Model):

    STATUS_READ = 1
    STATUS_NEW = 0
    STATUS_DELETED = -1
    STATUS_REJECTED = -3

    NOTIFICATION_STATUS_CHOICES = (
        (STATUS_READ, 'Read'),
        (STATUS_NEW, 'New'),
        (STATUS_DELETED, 'Deleted'),
        (STATUS_REJECTED, 'Rejected')
    )

    receiver = models.ForeignKey('party.Party', related_name='notification_receiver')
    actor = models.ForeignKey('party.Party', related_name='notification_actor')

    verb = models.ForeignKey(ContentType, related_name='notification_verb', null=True, blank=True)

    target_content_type = models.ForeignKey(ContentType, related_name='notification_target_content_type', null=True, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_id')

    organization = models.ForeignKey('organization.Organization', related_name='notification_organization', null=True, blank=True)
    party = models.ForeignKey('party.Party', related_name='notification_party', null=True,
                                     blank=True)
    status = models.IntegerField(choices=NOTIFICATION_STATUS_CHOICES, default=STATUS_NEW)

    created = models.DateTimeField()
    data = models.TextField(null=True, blank=True)

    # For happening
    is_system = models.NullBooleanField(null=True, blank=True)

    # Denormalize
    store_total_love = models.PositiveIntegerField(null=True, blank=True)


    cms = models.ManyToManyField('cms.CommonCms', related_name='notification_cms')


    @property
    def REQUIRED_APPROVAL(self):
        if hasattr(self.target, 'REQUIRED_APPROVAL'):
            return self.target.REQUIRED_APPROVAL
        return False
    

    def approval_required(self, request):

        dst_field = 'dst'
        if hasattr(self.target, 'swap') and self.target.swap:
            dst_field = 'src'

        return hasattr(self.target, 'REQUIRED_APPROVAL') and self.target.REQUIRED_APPROVAL and hasattr(self.target, dst_field) and \
               user_can_edit(request, getattr(self.target, dst_field))

    @property
    def approval_status(self):
        return self.target.status

    def is_love(self, logged_in_party):
        return bool(PartyLove.objects.filter(
            src=logged_in_party,
            dst_content_type=ContentType.objects.get_for_model(Notification),
            dst_id=self.id,
            status=STATUS_PUBLISHED
        ).count())

    def build_total(self, field_names=[]):

        if not self.id:
            return False

        if not field_names or ('total_love' in field_names):
            self.store_total_love = PartyLove.objects.filter(
                dst_content_type=ContentType.objects.get_for_model(self.__class__),
                dst_id=self.id,
                status=STATUS_PUBLISHED).count()

        self.save()

    @property
    def total_love(self):
        if self.store_total_love is None:
            self.build_total()
        return self.store_total_love



    # Magic  Helper Methods
    def get_html_display(self, display_created=True, display_icon=True, display_data=True, display_you=True):

        if not self.verb:
            return 'Something wrong in development process. Please, contact administrator'

        if display_you:
            receiver_name = 'you'
        else:
            if self.receiver.get_status() == STATUS_PUBLISHED:
                if not self.receiver.is_deleted:
                    receiver_name = '<a href="%s"><strong>%s</strong></a>' % (self.receiver.get_absolute_url(), self.receiver.get_display_name())
                else:
                    receiver_name = '<strong>%s</strong>' % (self.receiver.get_display_name())

            else:
                receiver_name = '<strong class="pending">%s (pending)</strong>' % (self.receiver.get_display_name())

        if self.organization:
            if self.organization.get_status() == STATUS_PUBLISHED:
                if not self.organization.is_deleted:
                    receiver_name = '<a href="%s"><strong class="your-admin">%s</strong></a>' % (self.organization.get_absolute_url(), self.organization.get_display_name())
                else:
                    receiver_name = '<strong class="your-admin">%s</strong>' % (self.organization.get_display_name())

            else:
                if not self.organization.is_deleted:
                    receiver_name = '<a href="%s"><strong class="your-admin">%s (pending)</strong></a>' % (self.organization.get_absolute_url(), self.organization.get_display_name())
                else:
                    receiver_name = '<strong class="your-admin">%s (pending)</strong>' % (self.organization.get_display_name())


        elif self.party:
            if self.party.get_status() == STATUS_PUBLISHED:
                if not self.party.is_deleted:
                    receiver_name = '<a href="%s"><strong>%s</strong></a>' % (self.party.get_absolute_url(), self.party.get_display_name())
                else:
                    receiver_name = '<strong>%s</strong>' % (self.party.get_display_name())

            else:
                receiver_name = '<strong class="pending">%s (pending)</strong>' % (self.party.get_display_name())




        Verb = self.verb.model_class()
        if hasattr(self.target, 'swap') and self.target.swap:
            verb_display = Verb.NOTIFICATION_VERB_SWAP_DISPLAY
        elif hasattr(self.target, 'system') and self.target.system:
            verb_display = Verb.NOTIFICATION_VERB_SYSTEM_DISPLAY
        else:
            try:
                verb_display = Verb.NOTIFICATION_VERB_DISPLAY
            except:
                verb_display = notification_m2m_verb_display[Verb]

        try:
            suffix = verb_display % receiver_name
        except TypeError:
            if self.actor.get_status() == STATUS_PUBLISHED:
                try:
                    self.target.get_absolute_url()
                    target_name = '<a href="%s"><strong>%s</strong></a>' % (self.target.get_absolute_url(), self.target)
                except:
                    target_name = '<strong>%s</strong>' % (self.target)

            else:
                target_name = '<strong class="pending">%s (pending)</strong>' % (self.target)


            suffix = verb_display % (receiver_name, target_name)


        if self.actor == self.receiver or (self.organization and self.actor.id == self.organization.id):
            html_display = suffix
        else:
            if self.party:
                if self.actor.get_status() == STATUS_PUBLISHED:
                    if not self.actor.is_deleted:
                        html_display = '<a href="%s"><strong class="your-following">%s</strong></a> %s' % (self.actor.get_absolute_url(), self.actor.get_display_name(), suffix)
                    else:
                        html_display = '<strong class="your-following">%s</strong> %s' % (self.actor.get_display_name(), suffix)

                else:
                    html_display = '<strong class="pending your-following">%s (pending)</strong> %s' % (self.actor.get_display_name(), suffix)

            else:

                if self.actor.get_status() == STATUS_PUBLISHED:
                    if not self.actor.is_deleted:
                        html_display = '<a href="%s"><strong>%s</strong></a> %s' % (self.actor.get_absolute_url(), self.actor.get_display_name(), suffix)
                    else:
                        html_display = '<strong>%s</strong> %s' % (self.actor.get_display_name(), suffix)

                else:
                    html_display = '<strong class="pending">%s (pending)</strong> %s' % (self.actor.get_display_name(), suffix)


        if hasattr(Verb, 'NOTIFICATION_DATE_FIELD'):
            date_field = getattr(Verb, 'NOTIFICATION_DATE_FIELD')
            date_value = getattr(self.target, date_field)

            if date_value:
                html_display = '%s on %s' % (html_display, date_value.strftime('%B %d, %Y'))

        # Force display data
        if hasattr(Verb, 'NOTIFICATION_DATA_FIELD'):
            display_data = True

        if display_data:
            if hasattr(Verb, 'NOTIFICATION_DATA_FIELD'):
                data_field = getattr(Verb, 'NOTIFICATION_DATA_FIELD')
                data_value = getattr_nested(self.target, data_field)

                if hasattr(Verb, 'NOTIFICATION_DATA_FIELD_IS_INTEGER'):
                    is_integer = getattr(Verb, 'NOTIFICATION_DATA_FIELD_IS_INTEGER')
                    if is_integer:
                        data_value = intcomma(int(data_value))

                if hasattr(Verb, 'NOTIFICATION_DATA_SUFFIX'):
                    data_value = '%s %s' % (data_value, self.target.NOTIFICATION_DATA_SUFFIX)

                target = self.target
                if hasattr(self.target, 'NOTIFICATION_TARGET_FIELD'):
                    target = getattr_nested(target, target.NOTIFICATION_TARGET_FIELD)


                html_display = '%s &nbsp;<a class="noti-data" href="%s">%s</a>' % (html_display, target.get_absolute_url(), data_value)

            elif hasattr(Verb, 'NOTIFICATION_DATA_DISPLAY') and Verb.NOTIFICATION_DATA_DISPLAY:
                html_display = '%s &nbsp;<a class="noti-data" href="%s">%s</a>' % (html_display, self.target.get_absolute_url(), Verb.NOTIFICATION_DATA_DISPLAY)
            elif hasattr(self.target, 'data') and self.target.data:

                if self.target.status == STATUS_PUBLISHED:
                    html_display = '%s &nbsp;"<a class="noti-data" href="%s">%s</a>"' % (html_display, self.target.get_absolute_url(), strip_tags(self.target.data)   )
                else:
                    html_display = '%s &nbsp;"<span class="noti-data" href="%s">%s</span>"' % (html_display, self.target.get_absolute_url(), strip_tags(self.target.data))


        if display_created:
            html_display = '%s <div class="date">%s</div>' % (html_display, self.created.strftime('%B %d, %Y'))

        if display_icon:

            if self.party:
                html_display = '<span class="icon your-following"></span> %s' % (html_display)
            else:
                html_display = '<span class="icon icon-noti-%s"></span> %s' % (self.verb.name.replace(' ', '-'), html_display)

            html_display = '<div class="notification-item-inner">%s</div>' % html_display


        return html_display


    def get_simple_html_display(self):
        return self.get_html_display(display_created=False, display_icon=False, display_data=False, display_you=False)

    def get_request_html_display(self):
        return self.get_html_display(display_created=True, display_icon=False, display_data=True, display_you=False)


def instance_is_created(instance, check_crazy_created=True, is_system=False, created=False):

    created_on_published = hasattr(instance, 'CREATED_ON_PUBLISHED') and instance.CREATED_ON_PUBLISHED

    if (created and not created_on_published) or (created and created_on_published and hasattr(instance, 'published') and instance.published):
        return created

    result1 = True
    result1 = result1 and instance.id


    if result1 and hasattr(instance, 'status'):
        result1 = result1 and (instance.status != STATUS_DRAFT)


    # Check status change from deleted to other
    result2 = True
    if result2 and not is_system and hasattr(instance, 'status') and hasattr(instance, 'var_cache'):
        origin_status = instance.var_cache.get('status')
        result2 = result2 and (origin_status == STATUS_DELETED)
        result2 = result2 and (instance.status in [STATUS_PENDING, STATUS_PUBLISHED])


    result2_1 = True
    if result2_1 and created_on_published and is_system and hasattr(instance, 'status') and hasattr(instance, 'var_cache'):
        origin_status = instance.var_cache.get('status')
        #origin_published = instance.var_cache.get('published')

        # TODO: fix case unpublish first to publish
        if created or instance.published:
            result2_1 = False
        else:
            result2_1 = result2_1 and (origin_status in [STATUS_DRAFT, STATUS_PENDING])
            result2_1 = result2_1 and (instance.status in [STATUS_PUBLISHED])


    result2_2 = True
    if result2_2 and is_system and hasattr(instance, 'is_active') and hasattr(instance, 'var_cache'):
        origin_is_active = instance.var_cache.get('is_active')
        result2_2 = result2_2 and not origin_is_active
        result2_2 = result2_2 and instance.is_active


    result3 = True
    if result3 and hasattr(instance, 'src') and hasattr(instance, 'var_cache'):
        origin_src = instance.var_cache.get('src')
        result3 = result3 and (origin_src is None)
        result3 = result3 and (instance.src is not None)


    result4 = True
    if result4 and hasattr(instance, 'dst') and hasattr(instance, 'var_cache'):
        origin_dst = instance.var_cache.get('dst')
        result4 = result4 and (origin_dst is None)
        result4 = result4 and (instance.dst is not None)



    return (result1 and ((result2 and result2_1 and result2_2) or (check_crazy_created and (result3 or result4))))


def instance_is_deleted(instance):
    result = False
    result = result or (hasattr(instance, 'is_deleted') and instance.is_deleted)
    result = result or (hasattr(instance, 'status') and instance.status == STATUS_DELETED)

    if hasattr(instance, 'status') and hasattr(instance, 'var_cache'):
        origin_status = instance.var_cache.get('status')
        result = result or ((origin_status in [STATUS_PUBLISHED]) and (instance.status in [STATUS_DRAFT, STATUS_PENDING]))

    return result




# Todo token link to setting form
def get_email_service_body(body, party):
    request = get_request()
    if request:
        current_site = get_current_site(request)
        site_name = current_site.name
    else:
        site_name = settings.SITE_NAME

    email = ''
    settings_url = ''

    if request:
        absolute_uri = request.build_absolute_uri('/')
    else:
        absolute_uri = settings.SITE_URL + '/'

    if party.__class__ is User:

        uid = urlsafe_base64_encode(force_bytes(party.pk))
        token = default_token_generator.make_token(party)

        body = body.replace('href="/', 'href="%s' % absolute_uri)

        settings_url = absolute_uri[0:-1] + reverse('account_settings_confirm', args=(uid, token))
        email = party.email

    elif party.__class__ is Organization:

        body = body.replace('href="/', 'href="%s' % absolute_uri)
        email = party.email_of_contact_person


    output = render_to_string('notification/email.html', {
        'body': body,
        'email': email,
        'site_name': site_name,
        'settings_url': settings_url
    })
    return output.replace('\n', '<br />')


def notification_send_email_helper(notification, email, receiver=False, email_body=False):

    receiver = receiver or notification.receiver.get_inst()

    email_from = '%s<message@%s>' % (notification.actor.get_display_name(), SITE_NAME)

    if not email_body:
        email_body = notification.get_html_display(display_created=False, display_icon=False)
    email_subject = re.sub('<span style="display:none".*?>.*?</span>', '', email_body)
    email_subject = strip_tags(email_subject)
    email_subject = email_subject[:30] + (email_subject[30:] and '...')
    email_body = get_email_service_body(email_body, receiver)

    send_mail(email_subject, email_body, email_from, [email], html_message=email_body, fail_silently=False)


def notification_send_email(notification, email_body=False):

    # Todo contact email is not here
    receiver = notification.receiver.get_inst()


    if not hasattr(receiver, 'email'):
        return

    print 'lllll'
    print notification.verb.app_label == 'forum'

    allow_send_mail = False
    if notification.organization:
        allow_field_name = 'notification_allow_email_send_organization_%s' % notification.verb.model
        if hasattr(receiver, allow_field_name) and getattr(receiver, allow_field_name):
            allow_send_mail = True

    elif notification.party:
        if receiver.notification_allow_email_send_from_follow:
            allow_send_mail = True

    elif notification.verb.app_label == 'forum':
        allow_send_mail = True

    else:
        allow_field_name = 'notification_allow_email_send_%s' % notification.verb.model
        if hasattr(receiver, allow_field_name) and getattr(receiver, allow_field_name):
            allow_send_mail = True


    if allow_send_mail:
        notification_send_email_helper(notification, receiver.email, receiver, email_body)


def notification_create_helper(instance, receiver, verb, target, actor, data=None, organization=None, party=None, is_system=None, allow_send_to_me=False, ignore_excludes=False, extra_emails=[]):
    # Make sure don't send to me
    if not allow_send_to_me and actor.id == receiver.id:
        return

    # Make sure don't send to inactive user
    deep_inst = receiver
    if hasattr(receiver, 'get_inst'):
        deep_inst = receiver.get_inst()
    else:
        # Force change receiver to self because is not a party (portfolio, jobs)
        target = receiver
        receiver = actor
        is_system = True

    #if hasattr(deep_inst, 'is_active') and not deep_inst.is_active:
    #    return
    #if hasattr(deep_inst, 'status') and deep_inst.status != STATUS_PUBLISHED:
    #    return

    # defind vale for created of notification
    created = timezone.now()

    # Happening use raw created from target or relation
    if hasattr(target, 'get_inst'):
        target = target.get_inst()

    if is_system:
        if hasattr(target, 'created') and target.created:
            created = target.created
        elif hasattr(target, 'created_raw') and target.created_raw:
            created = target.created_raw
        elif hasattr(target, 'date_joined') and target.date_joined:
            created = target.date_joined

    notification = Notification(
        receiver=receiver,
        verb=verb,
        target=target,
        actor=actor,
        data=data,
        organization=organization,
        party=party,
        status=Notification.STATUS_NEW,
        is_system=is_system,
        created=created
    )

    if ignore_excludes or (instance.__class__ not in notification_model_excludes):
        notification.save()

    notification_post_save_task.delay(notification, allow_create_notification, is_system, extra_emails)


@task
def notification_post_save_task(notification, allow_create_notification, is_system, extra_emails):


    print allow_create_notification, is_system
    print extra_emails

    # TODO: make to async
    if allow_create_notification and not is_system:
        notification_send_email(notification)

        for email in extra_emails:
            notification_send_email_helper(notification, email)

    # TODO: make to async
    if settings.FACEBOOK_PAGE_ID and settings.FACEBOOK_PAGE_ACCESS_TOKEN and notification.is_system and notification.verb:
        request = get_request()
        notification = Notification.objects.get(id=notification.id) # For fix duplicated actor (It work, I don't know why)

        share_obj = notification.target or notification.actor

        link = False

        if (hasattr(share_obj, 'image') and share_obj.image) or (hasattr(share_obj, 'images') and len(share_obj.images.all())):

            if request:
                absolute_uri = request.build_absolute_uri('/')
            else:
                absolute_uri = settings.SITE_URL + '/'

            try:
                link = absolute_uri + share_obj.get_absolute_url()
            except AttributeError:
                try:
                    link = '%s%s' % (settings.SITE_URL, share_obj.get_absolute_url())
                except AttributeError:
                    pass



        if link:
            data = {
                'access_token': settings.FACEBOOK_PAGE_ACCESS_TOKEN,
                'message': strip_tags(notification.get_simple_html_display()),
                'link': link
            }
            r = requests.post('https://graph.facebook.com/%s/feed' % settings.FACEBOOK_PAGE_ID, data=data)



def getattr_nested(obj, attrs):

    for attr in attrs.split('.'):
        obj = getattr(obj, attr)

    return obj


def notification_create(instance, is_system=False):
    data = None
    verb = ContentType.objects.get_for_model(instance)

    if hasattr(instance, 'data') and instance.data and instance.data not in ['example', 'sample']:
        data = instance.data

    allow_send_to_me = False

    if hasattr(instance, 'src'):
        actor = instance.src
        if not actor:
            return

    else:
        actor = instance
        allow_send_to_me = True


    target = instance
    if hasattr(target, 'party_ptr'):
        target = target.party_ptr

    if hasattr(instance, 'dst'):
        receiver = instance.dst
        if not receiver:
            return
    else:
        receiver = instance
        allow_send_to_me = True


    if hasattr(instance, 'swap') and instance.swap:
        swap = receiver
        receiver = actor
        actor = swap

    if hasattr(instance, 'NOTIFICATION_ACTOR_FIELD'):
        actor = getattr(actor, instance.NOTIFICATION_ACTOR_FIELD)

    if hasattr(actor, 'party_ptr'):
        actor = actor.party_ptr

    if receiver.__class__ is Notification:
        return

    # Send direct to receiver

    organization = receiver.get_inst()


    if hasattr(instance, 'system') and instance.system:
        is_system = True

        for staff in User.objects.filter(is_staff=True):
            notification_create_helper(
                instance=instance,
                receiver=staff,
                verb=verb,
                target=target,
                actor=actor,
                data=data,
                organization=organization,
                ignore_excludes=True,
            )


    if not is_system and allow_create_notification:

        extra_emails = []
        if hasattr(organization, 'email_of_contact_person') and organization.email_of_contact_person:
            extra_emails.append(organization.email_of_contact_person)

        notification_create_helper(
            instance=instance,
            receiver=receiver,
            verb=verb,
            target=target,
            actor=actor,
            data=data,
            allow_send_to_me=allow_send_to_me,
            extra_emails=extra_emails
        )


    # Send silent to sysem for list of happening
    notification_create_helper(
        instance=instance,
        receiver=receiver,
        verb=verb,
        target=target,
        actor=actor,
        data=data,
        is_system=True,
        allow_send_to_me=allow_send_to_me
    )

    if is_system or not allow_create_notification:
        return

    # Send notification to admins of organization
    admin_id_list = []
    if organization.__class__ is Organization and hasattr(organization, 'admins'):
        for admin in organization.admins.all():
            admin_id_list.append(admin.id)

            notification_create_helper(
                instance=instance,
                receiver=admin,
                verb=verb,
                target=target,
                actor=actor,
                data=data,
                organization=organization,
                ignore_excludes=True,
            )



    # Send notification to follower of actor
    actor_id_list = []

    for party_follow_party in PartyFollowParty.objects.filter(dst=actor, status=STATUS_PUBLISHED):
        follower = party_follow_party.src

        party = receiver
        if hasattr(party, 'party_ptr'):
            party = party.party_ptr

        if follower.id == party.id:
            continue

        if follower.id in admin_id_list:
            continue

        actor_id_list.append(follower.id)

        notification_create_helper(
            instance=instance,
            receiver=follower,
            verb=verb,
            target=target,
            actor=actor,
            data=data,
            party=party
        )

    # Send notification to follower of receiver
    if not hasattr(target, 'NOTIFICATION_PRIVATE') or (hasattr(target, 'NOTIFICATION_PRIVATE') and not target.NOTIFICATION_PRIVATE):
        for party_follow_party in PartyFollowParty.objects.filter(dst=receiver):
            follower = party_follow_party.src

            party = receiver
            if hasattr(party, 'party_ptr'):
                party = party.party_ptr

            if follower.id == party.id:
                continue

            if follower.id in admin_id_list:
                continue

            if follower.id in actor_id_list:
                continue

            notification_create_helper(
                instance=instance,
                receiver=follower,
                verb=verb,
                target=target,
                actor=actor,
                data=data,
                party=party
            )

# Signal



def notification_post_delete(sender, **kwargs):

    if not allow_create_notification:
        return

    instance = kwargs['instance']

    if sender._meta.app_label not in ['relation']:
        return

    verb = ContentType.objects.get_for_model(sender)

    Notification.objects.filter(verb=verb, target_id=instance.id).delete()


def notification_post_save(sender, **kwargs):

    instance = kwargs['instance']
    created = kwargs['created']
    update_fields = kwargs.get('update_fields') or []

    is_system = False
    if sender in notification_system_includes:
        is_system = True
        if not allow_create_notification:
            return

    if (sender._meta.app_label not in notification_app_includes) and (not is_system):
        return

    if not created and ('image' in update_fields or 'images' in update_fields or 'file' in update_fields or 'files' in update_fields):
        return

    verb = ContentType.objects.get_for_model(sender)

    if instance_is_deleted(instance):
        Notification.objects.filter(verb=verb, target_id=instance.id).delete()
        return

    if instance_is_created(instance, instance.NOTIFICATION_CHECK_CRAZY_CREATED, is_system=is_system, created=created):
        notification_create(instance, is_system=is_system)



def notification_m2m_changed(sender, **kwargs):

    if not allow_create_notification:
        return

    action = kwargs['action']
    instance = kwargs['instance']
    pk_set = kwargs['pk_set']
    model = kwargs['model']
    verb = ContentType.objects.get_for_model(sender)

    actor = instance
    if hasattr(actor, 'party_ptr'):
        actor = actor.party_ptr

    target = instance
    if hasattr(target, 'party_ptr'):
        target = target.party_ptr


    if sender in notification_m2m_includes and action == 'post_add':


        for receiver in model.objects.filter(id__in=pk_set):
            notification_create_helper(instance, receiver, verb, target, actor)

        if sender not in notification_m2m_private_includes:

            party_follow_party_list = list(PartyFollowParty.objects.filter(dst=actor, status=STATUS_PUBLISHED))
            for receiver in model.objects.filter(id__in=pk_set):
                for party_follow_party in party_follow_party_list:

                    follower = party_follow_party.src

                    party = actor
                    if hasattr(party, 'party_ptr'):
                        party = party.party_ptr

                    if follower.id == party.id:
                        continue

                    target = receiver

                    notification_create_helper(instance, follower, verb, target, actor, party=party)


post_save.connect(notification_post_save)
post_delete.connect(notification_post_delete)
m2m_changed.connect(notification_m2m_changed)
