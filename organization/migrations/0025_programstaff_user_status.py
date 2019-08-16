# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0024_auto_20180330_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='programstaff',
            name='user_status',
            field=models.IntegerField(default=100, choices=[(1, b'Mentor'), (100, b'Staff')]),
            preserve_default=True,
        ),
    ]
