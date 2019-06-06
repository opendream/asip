# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import re
import django.core.validators
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_organizationfunding_organizationgrowthstage_organizationproductlaunch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('permalink', models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')])),
                ('title', models.CharField(max_length=255)),
                ('title_th', models.CharField(max_length=255, null=True)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('summary_th', models.TextField(null=True, blank=True)),
                ('summary_en', models.TextField(null=True, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('description_th', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('description_en', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('priority', models.IntegerField(default=0)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='taxonomy.ArticleCategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
