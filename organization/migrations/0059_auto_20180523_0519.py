# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0058_auto_20180522_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='money_taken_equity_amount',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='money_taken_equity_amount_currency',
        ),
        migrations.AlterField(
            model_name='organization',
            name='taken_equity_amount',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
