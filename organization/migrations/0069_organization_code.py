# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0068_organization_is_mockup'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='code',
            field=models.CharField(max_length=512, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
