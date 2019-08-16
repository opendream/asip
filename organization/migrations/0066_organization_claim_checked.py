# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0065_auto_20180606_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='claim_checked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
