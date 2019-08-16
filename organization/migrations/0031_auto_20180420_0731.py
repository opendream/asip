# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_programtype_typeofassistantship_typeofattachment_typeofbatch_typeoffinancialsource_typeoffocusindust'),
        ('organization', '0030_auto_20180420_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='attachments_types',
            field=models.ManyToManyField(related_name='program_attachments_types', null=True, to='taxonomy.TypeOfAttachment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='focus_industry',
            field=models.ManyToManyField(related_name='program_focus_industry', null=True, to='taxonomy.TypeOfFocusIndustry', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='focus_sector',
            field=models.ManyToManyField(related_name='program_focus_sector', null=True, to='taxonomy.TypeOfFocusSector', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='investment_stage_type',
            field=models.ManyToManyField(related_name='program_investment_stage_type', null=True, to='taxonomy.TypeOfInvestmentStage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='investment_type',
            field=models.ManyToManyField(related_name='program_investment_type', null=True, to='taxonomy.TypeOfInvestment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='program_type',
            field=models.ManyToManyField(related_name='program_program_type', null=True, to='taxonomy.ProgramType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='stage_of_participants',
            field=models.ManyToManyField(related_name='program_stage_of_participants', null=True, to='taxonomy.TypeOfStageOfParticipant', blank=True),
            preserve_default=True,
        ),
    ]
