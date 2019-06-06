# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20160219_0640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='facebook_url',
        ),
        migrations.RemoveField(
            model_name='event',
            name='homepage_url',
        ),
        migrations.RemoveField(
            model_name='event',
            name='twitter_url',
        ),
        migrations.AddField(
            model_name='commoncms',
            name='facebook_url',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commoncms',
            name='homepage_url',
            field=models.URLField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commoncms',
            name='twitter_url',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=datetime.date(2016, 3, 4), null=True, blank=True),
            preserve_default=True,
        ),
    ]
