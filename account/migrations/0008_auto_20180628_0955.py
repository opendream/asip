# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_user_job_public_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='job_primary_role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='job_remote',
        ),
    ]
