# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='special',
            name='image',
            field=files_widget.fields.ImageField(max_length=200, null=True, verbose_name=b'Banner Image', blank=True),
            preserve_default=True,
        ),
    ]
