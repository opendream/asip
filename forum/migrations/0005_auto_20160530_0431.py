# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20160530_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumpost',
            name='parent',
            field=models.ForeignKey(related_name='posts', to='forum.ForumTopic'),
            preserve_default=True,
        ),
    ]
