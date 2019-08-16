# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0022_program_programbatch_programstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='investment_stage_type',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
