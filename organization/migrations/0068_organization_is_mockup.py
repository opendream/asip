# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0067_organization_published_claim'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_mockup',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
