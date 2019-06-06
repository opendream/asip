# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20160530_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumpost',
            name='files',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumreply',
            name='files',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
