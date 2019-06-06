# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('promote', models.NullBooleanField()),
                ('store_total_follower', models.PositiveIntegerField(null=True, blank=True)),
                ('store_total_following', models.PositiveIntegerField(null=True, blank=True)),
                ('store_total_love', models.PositiveIntegerField(null=True, blank=True)),
                ('store_total_testify', models.PositiveIntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(related_name='country', blank=True, to='taxonomy.Country', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('images', files_widget.fields.ImagesField(null=True, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('url', models.URLField(max_length=255, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='party',
            name='portfolios',
            field=models.ManyToManyField(related_name='party_portfolios', to='party.Portfolio'),
            preserve_default=True,
        ),
    ]
