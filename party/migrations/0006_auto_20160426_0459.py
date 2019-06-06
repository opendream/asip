# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0005_party_store_popular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='store_popular',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=10, blank=True),
            preserve_default=True,
        ),
    ]
