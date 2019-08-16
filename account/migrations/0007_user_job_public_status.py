# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180621_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job_public_status',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
