# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0004_auto_20160209_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='store_popular',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
