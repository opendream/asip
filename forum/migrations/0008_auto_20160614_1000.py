# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20160607_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forumboard',
            options={'ordering': ['-priority', 'created'], 'get_latest_by': 'created'},
        ),
        migrations.AddField(
            model_name='forumboard',
            name='priority',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
