# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.forms


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_auto_20160304_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='potential_size_of_investment',
            field=common.forms.BetterDecimalField(decimal_places=2, max_digits=19, blank=True, help_text=b'Potential size of investment in THB', null=True, verbose_name=b'Potential size of investment'),
            preserve_default=True,
        ),
    ]
