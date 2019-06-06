# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0002_remove_portfolio_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='portfolios',
            field=models.ManyToManyField(related_name='party_portfolios', null=True, to='party.Portfolio', blank=True),
            preserve_default=True,
        ),
    ]
