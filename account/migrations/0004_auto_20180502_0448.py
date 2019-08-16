# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_appconnect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=1, choices=[(b'M', 'Male'), (b'F', 'Female'), (b'N', 'Prefer not to say')]),
            preserve_default=True,
        ),
    ]
