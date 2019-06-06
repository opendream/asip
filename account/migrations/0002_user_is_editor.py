# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_editor',
            field=models.BooleanField(default=False, verbose_name='editor status'),
            preserve_default=True,
        ),
    ]
