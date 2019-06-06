# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_auto_20150429_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='country',
            field=models.ForeignKey(related_name='country', default=6, blank=True, to='taxonomy.Country', null=True),
            preserve_default=True,
        ),
    ]
