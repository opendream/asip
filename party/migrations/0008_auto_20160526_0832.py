# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0001_initial'),
        ('party', '0007_auto_20160426_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='special',
            field=models.ForeignKey(related_name='party_list', blank=True, to='special.Special', null=True),
            preserve_default=True,
        ),
    ]
