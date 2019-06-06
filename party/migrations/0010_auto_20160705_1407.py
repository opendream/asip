# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0009_auto_20160705_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='special',
        ),
    ]
