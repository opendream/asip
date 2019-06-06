from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
from account.models import User
from common.constants import STATUS_PUBLISHED, STATUS_CHOICES
from common.models import AbstractPermalink, CommonTrashModel
import files_widget
from notification.models import notification_create_helper
from special.models import Special


class BaseForum(CommonTrashModel):
    created_by = models.ForeignKey(User)

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PUBLISHED)

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    _form_url_name = 'forum'

    NOTIFICATION_CHECK_CRAZY_CREATED = False

    class Meta:
        abstract = True
        ordering = ['created']
        get_latest_by = 'created'

    def get_edit_url(self):

        if self.id:
            return reverse('%s_edit' % self.get_inst_type_display(), args=[self.id])

        return None

    def get_absolute_url(self):

        if self.id:
            arg = self.permalink if hasattr(self, 'permalink') else self.id
            return reverse('%s_detail' % self.get_inst_type_display(), args=[arg])

        return None

    def get_parent_model_class(self):

        model_class = self.__class__
        if hasattr(model_class, 'parent'):
            return model_class.parent.field.related.parent_model

    def get_parent_model_name(self):

        parent_model_class = self.get_parent_model_class()
        if parent_model_class:
            return parent_model_class().get_inst_type_human_readable().title()

    def user_can_edit(self, user):
        return user.is_staff or (user.id == self.created_by_id)

    def user_can_create(self, user):
        return user.is_staff

    def get_nested_all(self):
        nested_all = [self]

        instance = self
        while hasattr(instance, 'parent') and instance.parent:
            nested_all.append(instance.parent)
            instance = instance.parent


        nested_all.reverse()

        return nested_all




class Forum(BaseForum, AbstractPermalink):
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)

    parent = models.ForeignKey(Special, related_name='forums', null=True, blank=True)

    def user_can_edit(self, user):
        return user.is_staff

    def user_can_create(self, user):
        return user.is_staff


class ForumBoard(BaseForum, AbstractPermalink):
    parent = models.ForeignKey(Forum, related_name='boards')
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)

    priority = models.IntegerField(default=0)
    children_ordering = models.CharField(verbose_name='Topics Ordering', max_length=255, choices=(
        ('created', 'created'),
        ('-created', '-created'),
        ('title', 'title'),
        ('-title', '-title'),
    ), default='created')

    css_class = models.CharField(max_length=512, null=True, blank=True)


    class Meta:
        ordering = ['-priority', 'created']
        get_latest_by = 'created'

    def user_can_edit(self, user):
        return user.is_staff

    def user_can_create(self, user):
        return user.is_staff


class ForumTopic(BaseForum, AbstractPermalink):
    parent = models.ForeignKey(ForumBoard, related_name='topics')
    prefix = models.CharField(max_length=512, null=True, blank=True)
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    def user_can_edit(self, user):
        return user.is_staff

    def user_can_create(self, user):
        return user.is_staff

    def get_total_posts(self):
        return self.posts.all().count()

    def get_total_replies(self):
        return ForumReply.objects.filter(parent__parent=self).count()

class ForumPost(BaseForum):
    parent = models.ForeignKey(ForumTopic, related_name='posts')
    title = models.CharField(max_length=512, null=True, blank=True)

    description = RichTextField(null=True, blank=True)

    files = files_widget.XFilesField(verbose_name='File Attachment', null=True, blank=True)

    NOTIFICATION_VERB_DISPLAY = _('A new post has been added to %sr topic: "%s"')


    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'

    def __unicode__(self):
        return self.title

    def get_total_replies(self):
        return self.replies.all().count()

    def user_can_create(self, user):
        return user.is_authenticated()

    def save(self, *args, **kwargs):
        super(ForumPost, self).save(*args, **kwargs)

        notification_create_helper(
            instance=self,
            receiver=self.parent.created_by,
            verb=ContentType.objects.get_for_model(self),
            target=self,
            actor=self.created_by
        )





class ForumReply(BaseForum):
    parent = models.ForeignKey(ForumPost, related_name='replies')

    description = RichTextField(verbose_name='Your Answer')

    files = files_widget.XFilesField(verbose_name='File Attachment', null=True, blank=True)

    NOTIFICATION_VERB_DISPLAY = _('reply %sr post: "%s"')

    def __unicode__(self):
        return truncatewords(strip_tags(self.description), 10)

    def user_can_create(self, user):
        return user.is_authenticated()


    def save(self, *args, **kwargs):
        super(ForumReply, self).save(*args, **kwargs)

        notification_create_helper(
            instance=self,
            receiver=self.parent.created_by,
            verb=ContentType.objects.get_for_model(self),
            target=self,
            actor=self.created_by
        )
