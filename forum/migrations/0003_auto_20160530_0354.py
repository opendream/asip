# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20160530_0352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forumpost',
            old_name='images',
            new_name='files',
        ),
    ]
