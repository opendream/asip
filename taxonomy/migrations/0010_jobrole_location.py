# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import common.validators
import mptt.fields
import ckeditor.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0009_auto_20180522_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField(null=True, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('priority', models.IntegerField(default=0)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='taxonomy.JobRole', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField(null=True, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('priority', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-priority', 'id'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
