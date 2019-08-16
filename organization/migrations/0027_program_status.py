# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0026_auto_20180402_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='status',
            field=models.IntegerField(default=1, choices=[(100, b'Submitted'), (10, b'Edited'), (1, b'Draft')]),
            preserve_default=True,
        ),
    ]
