# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0010_organizationparticipate'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationparticipate',
            name='status',
            field=models.IntegerField(default=-1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft'), (-2, b'Deleted')]),
            preserve_default=True,
        ),
    ]
