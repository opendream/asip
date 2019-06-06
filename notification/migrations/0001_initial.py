# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20150429_1033'),
        ('party', '0003_auto_20150429_1033'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_id', models.PositiveIntegerField(null=True, blank=True)),
                ('status', models.IntegerField(default=0, choices=[(1, b'Read'), (0, b'New'), (-1, b'Deleted'), (-3, b'Rejected')])),
                ('created', models.DateTimeField()),
                ('data', models.TextField(null=True, blank=True)),
                ('is_system', models.NullBooleanField()),
                ('store_total_love', models.PositiveIntegerField(null=True, blank=True)),
                ('actor', models.ForeignKey(related_name='notification_actor', to='party.Party')),
                ('organization', models.ForeignKey(related_name='notification_organization', blank=True, to='organization.Organization', null=True)),
                ('party', models.ForeignKey(related_name='notification_party', blank=True, to='party.Party', null=True)),
                ('receiver', models.ForeignKey(related_name='notification_receiver', to='party.Party')),
                ('target_content_type', models.ForeignKey(related_name='notification_target_content_type', blank=True, to='contenttypes.ContentType', null=True)),
                ('verb', models.ForeignKey(related_name='notification_verb', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
