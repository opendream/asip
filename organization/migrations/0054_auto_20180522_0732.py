# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0053_auto_20180522_0707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='deal_size_end',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='deal_size_start',
        ),
    ]
