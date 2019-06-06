# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20160304_0726'),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='cms',
            field=models.ManyToManyField(related_name='notification_cms', to='cms.CommonCms'),
            preserve_default=True,
        ),
    ]
