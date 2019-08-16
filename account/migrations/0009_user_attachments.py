# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20180628_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='attachments',
            field=files_widget.fields.FilesField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
