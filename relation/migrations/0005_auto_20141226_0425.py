# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0004_partyinvestparty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyreceivedfundingparty',
            name='dst',
            field=models.ForeignKey(related_name='received_funding_dst', blank=True, to='party.Party', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partyreceivedinvestingparty',
            name='dst',
            field=models.ForeignKey(related_name='received_investing_dst', blank=True, to='party.Party', null=True),
            preserve_default=True,
        ),
    ]
