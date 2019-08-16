# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20180502_0448'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notification_allow_email_send_organization_organizationparticipate',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
    ]
