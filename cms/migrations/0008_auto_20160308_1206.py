# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20160304_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 8, 12, 6, 13, 248871, tzinfo=utc), null=True, blank=True),
            preserve_default=True,
        ),
    ]
