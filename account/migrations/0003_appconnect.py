# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_editor'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppConnect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('app_id', models.CharField(max_length=255, null=True, verbose_name=b'App ID', blank=True)),
                ('name', models.CharField(max_length=255)),
                ('site_uri', models.CharField(help_text=b'Exclude http or https, for development allow localhost', max_length=512, verbose_name=b'Site URI')),
                ('description', models.CharField(max_length=512, null=True, blank=True)),
                ('image', files_widget.fields.ImageField(max_length=200, null=True, verbose_name=b'Logo', blank=True)),
                ('created_by', models.ForeignKey(related_name='apps', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
