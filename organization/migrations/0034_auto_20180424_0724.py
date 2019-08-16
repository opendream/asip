# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_programtype_typeofassistantship_typeofattachment_typeofbatch_typeoffinancialsource_typeoffocusindust'),
        ('organization', '0033_auto_20180423_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='focus_industry',
            field=models.ManyToManyField(related_name='organization_focus_industry', null=True, to='taxonomy.TypeOfFocusIndustry', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='focus_sector',
            field=models.ManyToManyField(related_name='organization_focus_sector', null=True, to='taxonomy.TypeOfFocusSector', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='instagram_url',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='other_channel',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='other_focus_industry',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='other_focus_sector',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='preferred_name',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='stage_of_participants',
            field=models.ManyToManyField(related_name='organization_stage_of_participants', null=True, to='taxonomy.TypeOfStageOfParticipant', blank=True),
            preserve_default=True,
        ),
    ]
