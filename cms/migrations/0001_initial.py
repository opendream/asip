# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import datetime
import re
from django.conf import settings
import django.core.validators
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
        ('organization', '0006_auto_20150429_1033'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonCms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('title', models.CharField(max_length=255)),
                ('image', files_widget.fields.ImageField(max_length=200, null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('status', models.IntegerField(default=-1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('changed', models.DateTimeField(auto_now_add=True, null=True)),
                ('published', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('commoncms_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CommonCms')),
                ('location', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField(default=datetime.date(2016, 2, 9), null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('phone', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('facebook_url', models.URLField(max_length=255, null=True, blank=True)),
                ('twitter_url', models.URLField(max_length=255, null=True, blank=True)),
                ('homepage_url', models.URLField(max_length=255, null=True, blank=True)),
                ('organization', models.ForeignKey(related_name='event_organization', blank=True, to='organization.Organization', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.commoncms',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('commoncms_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CommonCms')),
                ('article_category', models.CharField(default=b'news', max_length=255, choices=[(b'news', b'News'), (b'knowledge-tools', b'Knowledge & Tools'), (b'service', b'Service')])),
                ('organization', models.ForeignKey(related_name='news_organization', blank=True, to='organization.Organization', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.commoncms',),
        ),
        migrations.AddField(
            model_name='commoncms',
            name='created_by',
            field=models.ForeignKey(related_name='news_created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commoncms',
            name='published_by',
            field=models.ForeignKey(related_name='news_published_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commoncms',
            name='topics',
            field=models.ManyToManyField(related_name='cms_topics', null=True, to='taxonomy.Topic', blank=True),
            preserve_default=True,
        ),
    ]
