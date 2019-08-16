# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0008_typeofoffice'),
        ('organization', '0050_auto_20180511_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='office_type',
            field=models.ManyToManyField(related_name='organization_office_type', null=True, to='taxonomy.TypeOfOffice', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='other_office_type',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
