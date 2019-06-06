import re
from datetime import date
import tagging
from ckeditor.fields import RichTextField
from django.core import validators
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from common.constants import SUMMARY_MAX_LENGTH, STATUS_PENDING, STATUS_PUBLISHED
from common.functions import instance_get_thumbnail
from common.models import PriorityModel, AbstractPermalink
import files_widget

from organization.models import Organization
from party.models import Party
from tagging_autocomplete_tagit.models import TagAutocompleteTagItField
from taxonomy.models import ArticleCategory

USER_MODEL = settings.AUTH_USER_MODEL

class CommonCms(AbstractPermalink):

    title = models.CharField(max_length=255)
    image = files_widget.ImageField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    topics = models.ManyToManyField('taxonomy.Topic', null=True, blank=True, related_name='cms_topics')
    party_created_by = models.ForeignKey(Party, related_name='cms_party_created_by')
    created_by = models.ForeignKey(USER_MODEL, related_name='cms_created_by')
    published_by = models.ForeignKey(USER_MODEL, related_name='cms_published_by', null=True, blank=True)

    status = models.IntegerField(default=STATUS_PUBLISHED)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed = models.DateTimeField(auto_now=True, null=True, blank=True)
    published = models.DateTimeField(null=True, blank=True)

    is_promoted = models.BooleanField(default=True)

    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    homepage_url = models.URLField(max_length=1024, null=True, blank=True)

    uuid = models.CharField(max_length=255, null=True, blank=True)



    class Meta:
        ordering = ['-id']

    def get_display_name(self):
        return self.title or ''

    def get_thumbnail(self):
        return instance_get_thumbnail(self, crop=None, size='x360')

    def get_thumbnail_in_primary(self):
        return instance_get_thumbnail(self, size='150x150', crop=None, upscale=False)

    def get_summary(self):
        return truncatechars(self.summary or self.description or '', SUMMARY_MAX_LENGTH)

    def get_absolute_url(self):

        if hasattr(self, 'news') and self.news:
            return self.news.get_absolute_url()
        elif hasattr(self, 'event') and self.event:
            return self.event.get_absolute_url()

        return ''

    def save(self, *args, **kwargs):
        super(CommonCms, self).save(*args, **kwargs)




class News(CommonCms):
    # relation
    #organization = models.ForeignKey(Organization, related_name='news_organization', null=True, blank=True)
    # Taxonomy
    ARTICLE_TYPE_CHOICES = (
        ('news', _('News')),
        ('knowledge-tools', _('Knowledge & Tools')),
    )
    # deprecate
    article_category = models.CharField(max_length=255, choices=ARTICLE_TYPE_CHOICES, default='news')

    categories = models.ManyToManyField('taxonomy.ArticleCategory', null=True, blank=True, related_name='cms_categories')

    tags = TagAutocompleteTagItField(max_tags=False, null=True, blank=True, max_length=2048)

    files = files_widget.XFilesField(verbose_name='File Attachment', null=True, blank=True)


    def get_absolute_url(self):

        first_category = None
        try:
            first_category = self.categories.filter(level=0).first()
        except (ArticleCategory.DoesNotExist, ValueError):

            try:
                first_category = self._categories[0]
            except (AttributeError, IndexError):
                pass

        if first_category:
            if first_category.permalink == 'news':
                return reverse('news_detail', args=[self.permalink, self.id])
            else:
                return reverse('article_detail', args=[first_category.permalink, self.permalink, self.id])

        # deprecate
        if self.article_category == 'news':
            return reverse('news_detail', args=[self.permalink, self.id])
        else:
            return reverse('article_detail', args=[self.article_category, self.permalink, self.id])

    def get_files(self):
        files = []
        if self.files:
            files = [ settings.MEDIA_URL + path  for path in self.files.split('\n')]

        return files


tagging.register(News, tag_descriptor_attr='tag_set')


class Event(CommonCms):

    #organization = models.ForeignKey(Organization, related_name='event_organization', null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=255, null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True
    )

    tags = TagAutocompleteTagItField(max_tags=False, null=True, blank=True, max_length=2048)


    def get_absolute_url(self):
        return reverse('event_detail', args=[self.permalink, self.id])

    def get_phones(self):
        return [phone.strip() for phone in self.phone.split(',')]

tagging.register(Event, tag_descriptor_attr='tag_set')
