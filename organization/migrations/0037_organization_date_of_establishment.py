# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0036_auto_20180426_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='date_of_establishment',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
