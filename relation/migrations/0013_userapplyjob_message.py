# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0012_userapplyjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapplyjob',
            name='message',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
