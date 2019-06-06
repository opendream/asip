# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
        ('party', '0004_auto_20160209_0902'),
        ('relation', '0006_partycontactparty_system'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmsHasParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft'), (-2, b'Deleted')])),
                ('dst', models.ForeignKey(related_name='cms_has_party_dst', to='party.Party')),
                ('src', models.ForeignKey(related_name='cms_has_party_src', to='cms.CommonCms')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
