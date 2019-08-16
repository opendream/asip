# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0061_auto_20180523_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='programbatch',
            name='amount_total_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programbatch',
            name='amount_pre_seed_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programbatch',
            name='amount_pre_series_a_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programbatch',
            name='amount_seed_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programbatch',
            name='amount_series_a_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programbatch',
            name='amount_series_b_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programbatch',
            name='amount_series_c_stage',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
    ]
