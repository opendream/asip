# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0042_auto_20180502_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='contact_information',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='contact_person',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
