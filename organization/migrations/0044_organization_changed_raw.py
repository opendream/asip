# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0043_auto_20180502_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='changed_raw',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
