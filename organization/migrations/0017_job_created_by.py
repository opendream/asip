# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0016_auto_20160405_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='created_by',
            field=models.ForeignKey(related_name='job_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
