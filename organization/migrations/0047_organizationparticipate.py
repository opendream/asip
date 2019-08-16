# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0046_program_is_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationParticipate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.PositiveIntegerField(null=True, blank=True)),
                ('organization', models.ForeignKey(related_name='organization_participate', to='organization.Organization')),
                ('program', models.ForeignKey(related_name='program_participate', to='organization.Program')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
