# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0010_jobrole_location'),
        ('organization', '0069_organization_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_primary_role',
            field=models.ForeignKey(related_name='job_job_primary_role', blank=True, to='taxonomy.JobRole', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='job_roles',
            field=models.ManyToManyField(related_name='job_job_roles', null=True, to='taxonomy.JobRole', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='locations',
            field=models.ManyToManyField(to='taxonomy.Location', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='position',
            field=models.CharField(blank=True, max_length=128, null=True, choices=[(b'full-time', 'Full Time'), (b'contract', 'Contract'), (b'internship', 'Internship'), (b'cofounder', 'Cofounder')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='remote',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
