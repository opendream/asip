# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0023_program_investment_stage_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='programbatch',
            name='program',
            field=models.ForeignKey(related_name='batch_program', default=1, to='organization.Program'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programstaff',
            name='program',
            field=models.ForeignKey(related_name='staff_program', default=1, to='organization.Program'),
            preserve_default=False,
        ),
    ]
