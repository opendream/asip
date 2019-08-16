# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0008_auto_20180522_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyreceivedfundingparty',
            name='money_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partyreceivedinvestingparty',
            name='money_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
    ]
