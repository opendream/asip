# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0004_auto_20160209_0902'),
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='news',
            name='organization',
        ),
        migrations.AddField(
            model_name='commoncms',
            name='is_promoted',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commoncms',
            name='party_created_by',
            field=models.ForeignKey(related_name='cms_party_created_by', blank=True, to='party.Party', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commoncms',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commoncms',
            name='created_by',
            field=models.ForeignKey(related_name='cms_created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commoncms',
            name='published_by',
            field=models.ForeignKey(related_name='cms_published_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=datetime.date(2016, 2, 10), null=True, blank=True),
            preserve_default=True,
        ),
    ]
