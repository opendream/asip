import copy
from uuid import uuid1
import bleach
from datetime import datetime, timedelta
from haystack.indexes import SearchIndex
import ckeditor
from django.conf import settings
from django.core import validators
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


import re
from common.constants import NO_IP, STATUS_PENDING, STATUS_CHOICES
from common.functions import common_clean, get_ip_address, camelcase_to_underscore
from common.signals import get_request
from common.validators import validate_reserved_url


class CommonTrashManager(models.Manager):
    def filter_without_trash(self, *args, **kwargs):
        if not kwargs.get('is_deleted'):
            return super(CommonTrashManager, self).filter(*args, **kwargs).exclude(is_deleted=True)
        else:
            return super(CommonTrashManager, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        if not kwargs.get('is_deleted'):
            return super(CommonTrashManager, self).exclude(*args, **kwargs).exclude(is_deleted=True)

    def filter(self, *args, **kwargs):
        return self.filter_without_trash(*args, **kwargs)

    def all(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def get_without_trash(self, *args, **kwargs):
        if not kwargs.get('is_deleted'):
            kwargs['is_deleted'] = False
        return super(CommonTrashManager, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.get_without_trash(*args, **kwargs)

    def annotate(self, *args, **kwargs):
        return super(CommonTrashManager, self).exclude(is_deleted=True).annotate(*args, **kwargs)


class CommonModel(models.Model):

    @property
    def inst_name(self):
        return _(self.__class__.__name__)

    @property
    def inst_type(self):
        return self.__class__.__name__

    def get_inst_type_display(self):
        return camelcase_to_underscore(self.inst_type)

    def get_inst_type_human_readable(self):
        return _(self.get_inst_type_display().replace('_', ' '))

    def get_class_display(self):
        return self.inst_name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        for field in self._meta.fields:
            if type(field) in [ckeditor.fields.RichTextField]:
                value = common_clean(getattr(self, field.name))
                setattr(self, field.name, value)
            elif type(field) in [models.fields.CharField, models.fields.TextField]:
                #value = bleach.clean(getattr(self, field.name))
                #setattr(self, field.name, value)
                pass

        super(CommonModel, self).save(*args, **kwargs)


class CommonTrashModel(CommonModel):
    is_deleted = models.BooleanField(default=False)
    objects = CommonTrashManager()

    def save(self, *args, **kwargs):
        super(CommonTrashModel, self).save(*args, **kwargs)


    def trash(self, *args, **kwargs):

        self.is_deleted = True

        deleted_uuid = str(uuid1())[0: 10].replace('-', '')
        if hasattr(self, 'permalink'):
            self.permalink = 'deleted_%s_%s' % (deleted_uuid, self.permalink)
        # Common for delete user
        if hasattr(self, 'username'):
            self.email = 'deleted_%s_%s' % (deleted_uuid, self.username)
        if hasattr(self, 'email'):
            self.email = 'deleted_%s_%s' % (deleted_uuid, self.email)

        self.save()
        return self

    def delete(self, *args, **kwargs):
        return self.trash(self, *args, **kwargs)

    def remove(self, *args, **kwargs):
        return super(CommonTrashModel, self).delete(*args, **kwargs)

    @property
    def total_views(self):

        content_type = ContentType.objects.get_for_model(self)

        try:
            return StatisitcTotal.objects.get(content_type=content_type, object_id=self.id).value
        except StatisitcTotal.DoesNotExist:
            return 0
        except StatisitcTotal.MultipleObjectsReturned:
            statisitc_total = StatisitcTotal.objects.filter(content_type=content_type, object_id=self.id).latest('id')
            StatisitcTotal.objects.filter(content_type=content_type, object_id=self.id, id__lt=statisitc_total.id).delete()
            return statisitc_total.value

    class Meta:
        abstract = True


class CachedModel(models.Model):

    cached_vars = ['status', 'src', 'dst', 'is_active', 'published']

    def __init__(self, *args, **kwargs):
        super(CachedModel, self).__init__(*args, **kwargs)
        self.var_cache = {}
        for var in self.cached_vars:
            try:
                self.var_cache[var] = copy.copy(getattr(self, var))
            except:
                self.var_cache[var] = None

    class Meta:
        abstract = True


class AbstractPermalink(CommonModel):

    class Meta:
        abstract = True

    permalink = models.CharField(max_length=255, unique=True,
        help_text=_('Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters'),
        validators=[
            validate_reserved_url,
            validators.RegexValidator(re.compile('^[\w.+-]+$'), _('Enter a valid permalink.'), 'invalid'),
        ])

    def __unicode__(self):
        return self.permalink


class PriorityModel(models.Model):

    priority = models.PositiveIntegerField(default=0)
    ordering = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Logic make from "test_uptodate_status (domain.tests.test_model.TestStatement)"

        if not self.id:
            super(PriorityModel, self).save(*args, **kwargs)
            #instance = self.objects.get(id=self.id)
            self.save()
        else:
            self.ordering = int('%s%s' % (('0' * 2 + '%s' % self.priority)[-2:], ('0' * 8 + '%s' % self.id)[-8:]))
            super(PriorityModel, self).save(*args, **kwargs)


class StatisitcTotal(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    value = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super(StatisitcTotal, self).save(*args, **kwargs)
        if hasattr(self.content_object, 'build_total'):
            self.content_object.build_total(field_names=['popular'])


class StatisitcAccess(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(default=NO_IP)

    def save(self, *args, **kwargs):

        if not self.ip_address:
            self.ip_address = get_ip_address(get_request())

        is_flush = StatisitcAccess.objects.filter(
            object_id=self.object_id,
            content_type=self.content_type,
            ip_address=self.ip_address,
            created__gt=datetime.now() - timedelta(days=1)
        ).count()

        if is_flush:
            return

        super(StatisitcAccess, self).save(*args, **kwargs)

        try:
            total = StatisitcTotal.objects.get(content_type=self.content_type, object_id=self.object_id)
            total.value = total.value + 1
            total.save()

        except StatisitcTotal.DoesNotExist:
            StatisitcTotal.objects.create(content_type=self.content_type, object_id=self.object_id, value=1)

