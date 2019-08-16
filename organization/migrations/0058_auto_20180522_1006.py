# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0057_auto_20180522_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='money_salary_max',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='money_salary_min',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='money_deal_size_end',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='money_deal_size_start',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='money_taken_equity_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
    ]
