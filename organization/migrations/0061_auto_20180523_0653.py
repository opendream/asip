# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0060_auto_20180523_0533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='amount_of_money_invested',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='money_raise',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='pre_money_valuation',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='target_funding',
        ),
        migrations.AddField(
            model_name='organization',
            name='money_amount_of_money_invested',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_amount_of_money_invested_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_money_raise',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_money_raise_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_pre_money_valuation',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_pre_money_valuation_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_target_funding',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_target_funding_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
    ]
