# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0010_auto_20160705_1407'),
        ('notification', '0002_notification_cms'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='origin_receiver',
            field=models.ForeignKey(related_name='notification_origin_receiver', blank=True, to='party.Party', null=True),
            preserve_default=True,
        ),
    ]
