# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0006_auto_20160426_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='store_popular',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=8, blank=True),
            preserve_default=True,
        ),
    ]
