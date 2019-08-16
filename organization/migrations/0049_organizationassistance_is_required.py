# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0048_organization_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationassistance',
            name='is_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
