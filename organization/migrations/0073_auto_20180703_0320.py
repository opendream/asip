# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0072_auto_20180628_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='attachments',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staff',
            name='attachments',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
