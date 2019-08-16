# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_programtype_typeofassistantship_typeofattachment_typeofbatch_typeoffinancialsource_typeoffocusindust'),
        ('organization', '0029_auto_20180420_0727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='attachments_information',
        ),
        migrations.RemoveField(
            model_name='program',
            name='focus_industry',
        ),
        migrations.RemoveField(
            model_name='program',
            name='focus_sector',
        ),
        migrations.RemoveField(
            model_name='program',
            name='investment_stage_type',
        ),
        migrations.RemoveField(
            model_name='program',
            name='investment_type',
        ),
        migrations.RemoveField(
            model_name='program',
            name='program_type',
        ),
        migrations.RemoveField(
            model_name='program',
            name='stage_of_participants',
        ),
        migrations.AddField(
            model_name='programbatch',
            name='batch_type',
            field=models.ForeignKey(related_name='batch_type_program', blank=True, to='taxonomy.TypeOfBatch', null=True),
            preserve_default=True,
        ),
    ]
