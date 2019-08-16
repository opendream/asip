# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0065_auto_20180606_0649'),
        ('relation', '0009_auto_20180522_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationParticipate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('month', models.PositiveIntegerField(null=True, blank=True)),
                ('dst', models.ForeignKey(related_name='participate_dst', to='organization.Program')),
                ('src', models.ForeignKey(related_name='participate_src', to='organization.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
