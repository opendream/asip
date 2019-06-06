# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_remove_job_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type_of_organization',
            field=models.CharField(default=b'social-enterprise', max_length=128, choices=[(b'social-enterprise', 'Social Enterprise'), (b'supporter', 'Supporters/Investors')]),
            preserve_default=True,
        ),
    ]
