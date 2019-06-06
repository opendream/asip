# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20160614_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumboard',
            name='children_ordering',
            field=models.CharField(default=b'created', max_length=255, choices=[(b'created', b'created'), (b'-created', b'-created'), (b'title', b'title'), (b'-title', b'-title')]),
            preserve_default=True,
        ),
    ]
