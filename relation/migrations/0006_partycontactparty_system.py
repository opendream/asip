# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0005_auto_20141226_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='partycontactparty',
            name='system',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
