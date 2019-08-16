# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0025_programstaff_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programstaff',
            name='user_status',
        ),
        migrations.AddField(
            model_name='programstaff',
            name='staff_status',
            field=models.IntegerField(default=1, choices=[(100, b'Mentor'), (1, b'Staff')]),
            preserve_default=True,
        ),
    ]
