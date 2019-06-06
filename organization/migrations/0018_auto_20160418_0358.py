# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0017_job_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='jobs',
            field=models.ManyToManyField(related_name='organization_jobs', null=True, to='organization.Job', blank=True),
            preserve_default=True,
        ),
    ]
