# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0071_job_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='money_salary_max_thb',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='money_salary_max_usd',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='money_salary_min_thb',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='money_salary_min_usd',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='position',
            field=models.CharField(blank=True, max_length=128, null=True, choices=[(b'full-time', 'Full-time Employee'), (b'contract', 'Contractor'), (b'internship', 'Intern'), (b'cofounder', 'Co-founder')]),
            preserve_default=True,
        ),
    ]
