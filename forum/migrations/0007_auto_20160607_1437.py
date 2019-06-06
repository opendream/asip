# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0001_initial'),
        ('forum', '0006_auto_20160530_0958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forum',
            options={'ordering': ['created'], 'get_latest_by': 'created'},
        ),
        migrations.AlterModelOptions(
            name='forumboard',
            options={'ordering': ['created'], 'get_latest_by': 'created'},
        ),
        migrations.AlterModelOptions(
            name='forumpost',
            options={'ordering': ['-created'], 'get_latest_by': 'created'},
        ),
        migrations.AlterModelOptions(
            name='forumreply',
            options={'ordering': ['created'], 'get_latest_by': 'created'},
        ),
        migrations.AlterModelOptions(
            name='forumtopic',
            options={'ordering': ['created'], 'get_latest_by': 'created'},
        ),
        migrations.AddField(
            model_name='forum',
            name='parent',
            field=models.ForeignKey(related_name='forums', blank=True, to='special.Special', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumpost',
            name='files',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'File Attachment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumreply',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name=b'Your Answer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumreply',
            name='files',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'File Attachment', blank=True),
            preserve_default=True,
        ),
    ]
