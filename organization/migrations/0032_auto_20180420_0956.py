# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0031_auto_20180420_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='other_focus_industry',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='other_focus_sector',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
