# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0028_auto_20180420_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('job_title', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('contact_number', models.CharField(max_length=100, null=True, blank=True)),
                ('attachments', files_widget.fields.FilesField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramStaff',
            fields=[
                ('staff_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='organization.Staff')),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('staff_status', models.IntegerField(default=1, choices=[(100, 'Mentor'), (1, 'Staff')])),
                ('program', models.ForeignKey(related_name='staff_program', to='organization.Program')),
            ],
            options={
                'abstract': False,
            },
            bases=('organization.staff', models.Model),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(related_name='user_staff', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
