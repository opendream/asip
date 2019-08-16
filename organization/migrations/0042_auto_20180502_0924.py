# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0041_auto_20180502_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type_of_organization',
            field=models.CharField(default=b'startup', max_length=128, choices=[(b'startup', 'Startup'), (b'program', 'Program'), (b'supporter', 'Supporters/Investors')]),
            preserve_default=True,
        ),
    ]
