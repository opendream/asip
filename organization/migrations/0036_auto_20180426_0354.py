# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0035_auto_20180424_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationstaff',
            name='organization',
            field=models.ForeignKey(related_name='staff_organization', blank=True, to='organization.Organization', null=True),
            preserve_default=True,
        ),
    ]
