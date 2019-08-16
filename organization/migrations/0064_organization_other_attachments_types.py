# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0063_programbatch_amount_specific_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='other_attachments_types',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
    ]
