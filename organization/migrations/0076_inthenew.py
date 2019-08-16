# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0075_auto_20190208_0405'),
    ]

    operations = [
        migrations.CreateModel(
            name='InTheNew',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('date', models.DateField(null=True, blank=True)),
                ('title', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', files_widget.fields.ImageField(max_length=200, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(to='organization.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
