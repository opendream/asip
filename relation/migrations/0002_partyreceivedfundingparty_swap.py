# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partyreceivedfundingparty',
            name='swap',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
