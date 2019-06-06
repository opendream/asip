# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_forumboard_children_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumtopic',
            name='prefix',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumboard',
            name='children_ordering',
            field=models.CharField(default=b'created', max_length=255, verbose_name=b'Topics Ordering', choices=[(b'created', b'created'), (b'-created', b'-created'), (b'title', b'title'), (b'-title', b'-title')]),
            preserve_default=True,
        ),
    ]
