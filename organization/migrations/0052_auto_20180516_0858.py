# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0051_auto_20180514_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='organization',
            field=models.ForeignKey(related_name='program_organization', blank=True, to='organization.Organization', null=True),
            preserve_default=True,
        ),
    ]
