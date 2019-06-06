from django.db import models

# Create your models here.
from common.constants import STATUS_PUBLISHED, STATUS_CHOICES
from common.models import AbstractPermalink, CommonTrashModel
import files_widget


class Special(CommonTrashModel, AbstractPermalink):
    title = models.CharField(max_length=512)
    image = files_widget.ImageField(verbose_name='Banner Image', null=True, blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PUBLISHED)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __unicode__(self):
        return self.permalink

    def get_absolute_url(self):
        return '/%s/' % self.permalink


class Page(CommonTrashModel, AbstractPermalink):

    special = models.ForeignKey(Special, related_name='pages', null=True, blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PUBLISHED)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, null=True, blank=True)
