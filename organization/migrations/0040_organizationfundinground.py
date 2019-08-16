# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0039_auto_20180426_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationFundingRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('announced_date', models.DateField(null=True, blank=True)),
                ('closed_date', models.DateField(null=True, blank=True)),
                ('organization', models.ForeignKey(related_name='funding_round_organization', to='organization.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
