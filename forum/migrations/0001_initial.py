# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import re
import common.validators
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='boards', to='forum.Forum')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512, null=True, blank=True)),
                ('images', files_widget.fields.ImagesField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='posts', to='forum.ForumBoard')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('images', files_widget.fields.ImagesField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='replies', to='forum.ForumPost')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='topics', to='forum.ForumBoard')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
