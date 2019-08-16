# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0076_inthenew'),
    ]

    operations = [
        migrations.CreateModel(
            name='InTheNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('date', models.DateField(null=True, blank=True)),
                ('title', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', files_widget.fields.ImageField(max_length=200, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='inthenew',
            name='organization',
        ),
        migrations.DeleteModel(
            name='InTheNew',
        ),
        migrations.AddField(
            model_name='organization',
            name='in_the_news',
            field=models.ManyToManyField(related_name='organization_in_the_news', null=True, to='organization.InTheNews', blank=True),
            preserve_default=True,
        ),
    ]
