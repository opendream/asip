# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160523_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='files',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'File Attachment', blank=True),
            preserve_default=True,
        ),
    ]
