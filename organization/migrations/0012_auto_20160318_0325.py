# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0011_auto_20160308_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type_of_organization',
            field=models.CharField(default=b'startup', max_length=128, choices=[(b'startup', 'Startup'), (b'supporter', 'Supporters/Investors')]),
            preserve_default=True,
        ),
    ]
