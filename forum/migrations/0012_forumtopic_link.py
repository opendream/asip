# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_forumboard_css_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumtopic',
            name='link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
