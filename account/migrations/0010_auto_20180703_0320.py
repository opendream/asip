# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_user_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job_email',
            field=models.EmailField(max_length=255, null=True, verbose_name='job email address', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_telephone',
            field=models.CharField(max_length=255, null=True, verbose_name='job telephone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='attachments',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
