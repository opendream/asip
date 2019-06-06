# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '__first__'),
        ('relation', '0003_partyreceivedinvestingparty'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyInvestParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=-1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft'), (-2, b'Deleted')])),
                ('swap', models.NullBooleanField()),
                ('dst', models.ForeignKey(related_name='invest_dst', to='party.Party')),
                ('src', models.ForeignKey(related_name='invest_src', to='party.Party')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
