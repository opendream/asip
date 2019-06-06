# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20160315_0509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commoncms',
            old_name='tags',
            new_name='cms_tags',
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, null=True, blank=True),
            preserve_default=True,
        ),
    ]
