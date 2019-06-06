# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_investortype'),
        ('organization', '0012_auto_20160318_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='investor_type',
            field=models.ForeignKey(related_name='investor_type', blank=True, to='taxonomy.InvestorType', null=True),
            preserve_default=True,
        ),
    ]
