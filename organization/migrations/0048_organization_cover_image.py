# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0047_organizationparticipate'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='cover_image',
            field=files_widget.fields.ImageField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
