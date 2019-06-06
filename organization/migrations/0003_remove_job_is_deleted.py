# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20141225_0412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='is_deleted',
        ),
    ]
