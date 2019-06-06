# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging_autocomplete_tagit.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20160315_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=tagging_autocomplete_tagit.models.TagAutocompleteTagItField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=tagging_autocomplete_tagit.models.TagAutocompleteTagItField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
    ]
