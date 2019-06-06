# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0015_auto_20160420_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commoncms',
            name='party_created_by',
            field=models.ForeignKey(related_name='cms_party_created_by', to='party.Party'),
            preserve_default=True,
        ),
    ]
