# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0072_auto_20180628_0955'),
        ('relation', '0011_organizationparticipate_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserApplyJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=-1, choices=[(1, 'Published'), (-1, 'Request for Approval'), (0, 'Draft'), (-2, b'Deleted')])),
                ('dst', models.ForeignKey(related_name='user_apply_job_dst', to='organization.Organization')),
                ('job', models.ForeignKey(related_name='user_apply_job_job', to='organization.Job')),
                ('src', models.ForeignKey(related_name='user_apply_job_src', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
