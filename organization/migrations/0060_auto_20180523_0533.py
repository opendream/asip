# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0059_auto_20180523_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='amount_of_financial_supports',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
