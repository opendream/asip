# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0021_auto_20161004_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('program_type', models.CharField(max_length=128, null=True, blank=True)),
                ('date_of_establishment', models.DateField(null=True, blank=True)),
                ('contact_information', models.TextField(null=True, blank=True)),
                ('contact_person', models.TextField(null=True, blank=True)),
                ('focus_sector', models.TextField(null=True, blank=True)),
                ('focus_industry', models.TextField(null=True, blank=True)),
                ('stage_of_participants', models.TextField(null=True, blank=True)),
                ('is_acting_as_an_investor', models.BooleanField(default=False)),
                ('has_invited_in_participants_team', models.BooleanField(default=False)),
                ('investment_type', models.TextField(null=True, blank=True)),
                ('has_specific_stage', models.BooleanField(default=False)),
                ('specific_stage', models.TextField(null=True, blank=True)),
                ('has_taken_equity_in_participating_team', models.BooleanField(default=False)),
                ('does_provide_financial_supports', models.BooleanField(default=False)),
                ('amount_of_financial_supports', models.PositiveIntegerField(null=True, blank=True)),
                ('period_of_engagement', models.PositiveIntegerField(null=True, blank=True)),
                ('does_provide_working_spaces', models.BooleanField(default=False)),
                ('working_spaces_information', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('is_own_working_space', models.BooleanField(default=False)),
                ('does_provide_service_and_facility', models.BooleanField(default=False)),
                ('service_and_facility_information', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('attachments_information', models.TextField(null=True, blank=True)),
                ('attachments', files_widget.fields.FilesField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='program_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('organization', models.ForeignKey(related_name='program_organization', to='organization.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('has_pre_seed_stage', models.BooleanField(default=False)),
                ('has_seed_stage', models.BooleanField(default=False)),
                ('has_pre_series_a_stage', models.BooleanField(default=False)),
                ('has_series_a_stage', models.BooleanField(default=False)),
                ('has_series_b_stage', models.BooleanField(default=False)),
                ('has_series_c_stage', models.BooleanField(default=False)),
                ('amount_pre_seed_stage', models.PositiveIntegerField(null=True, blank=True)),
                ('amount_seed_stage', models.PositiveIntegerField(null=True, blank=True)),
                ('amount_pre_series_a_stage', models.PositiveIntegerField(null=True, blank=True)),
                ('amount_series_a_stage', models.PositiveIntegerField(null=True, blank=True)),
                ('amount_series_b_stage', models.PositiveIntegerField(null=True, blank=True)),
                ('amount_series_c_stage', models.PositiveIntegerField(null=True, blank=True)),
                ('total_teams_applying', models.TextField(null=True, blank=True)),
                ('total_teams_accepted', models.TextField(null=True, blank=True)),
                ('total_participants_accepted', models.TextField(null=True, blank=True)),
                ('total_graduated_teams_accepted', models.TextField(null=True, blank=True)),
                ('total_training_program', models.TextField(null=True, blank=True)),
                ('total_organized_event', models.TextField(null=True, blank=True)),
                ('total_coached_staff', models.TextField(null=True, blank=True)),
                ('total_assisting_staff', models.TextField(null=True, blank=True)),
                ('total_approximated_products', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramStaff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=512)),
                ('job_title', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('contact_number', models.CharField(max_length=100, null=True, blank=True)),
                ('attachments', files_widget.fields.FilesField(null=True, blank=True)),
                ('user', models.ForeignKey(related_name='program_staff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
