# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0045_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='is_partner',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
