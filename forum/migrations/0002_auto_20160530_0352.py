# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumreply',
            name='images',
        ),
        migrations.AddField(
            model_name='forumreply',
            name='files',
            field=files_widget.fields.FilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumpost',
            name='description',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumreply',
            name='description',
            field=ckeditor.fields.RichTextField(default=''),
            preserve_default=False,
        ),
    ]
