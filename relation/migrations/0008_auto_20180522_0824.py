# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0007_cmshasparty'),
    ]

    operations = [
        migrations.AddField(
            model_name='partyreceivedfundingparty',
            name='money_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=10, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partyreceivedfundingparty',
            name='money_amount_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partyreceivedinvestingparty',
            name='money_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=10, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partyreceivedinvestingparty',
            name='money_amount_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
    ]
