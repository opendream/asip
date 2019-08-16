# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0062_auto_20180601_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='programbatch',
            name='amount_specific_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
    ]
