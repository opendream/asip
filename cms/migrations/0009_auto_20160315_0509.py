# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging_autocomplete_tagit.models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_auto_20160308_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='commoncms',
            name='tags',
            field=tagging_autocomplete_tagit.models.TagAutocompleteTagItField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commoncms',
            name='status',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 15, 5, 9, 37, 717982, tzinfo=utc), null=True, blank=True),
            preserve_default=True,
        ),
    ]
