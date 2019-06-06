# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0013_organization_investor_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='point',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
