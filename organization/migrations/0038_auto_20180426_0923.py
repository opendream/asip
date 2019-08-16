# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_programtype_typeofassistantship_typeofattachment_typeofbatch_typeoffinancialsource_typeoffocusindust'),
        ('organization', '0037_organization_date_of_establishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='funding_type',
            field=models.ManyToManyField(related_name='organization_funding', null=True, to='taxonomy.TypeOfFunding', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='has_taken_equity',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='taken_equity_amount',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
