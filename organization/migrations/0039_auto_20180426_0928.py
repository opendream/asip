# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0038_auto_20180426_0923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='has_taken_equity',
            new_name='has_taken_equity_in_startup',
        ),
    ]
