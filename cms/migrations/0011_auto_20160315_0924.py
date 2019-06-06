# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging_autocomplete_tagit.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20160315_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commoncms',
            name='cms_tags',
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=tagging_autocomplete_tagit.models.TagAutocompleteTagItField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=tagging_autocomplete_tagit.models.TagAutocompleteTagItField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
