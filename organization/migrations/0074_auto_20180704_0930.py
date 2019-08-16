# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0073_auto_20180703_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='attachments_biography_consisting_of_major_achievements_of_management_levels',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_financial_statement',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_incorporation_registration_certificate',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_investment_portfolio',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_list_of_notable_startup_team_alumni',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_list_of_organization_or_program_partners',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_list_of_organizational_or_program_partners',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_long_term_sustainable_revenue_model',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_other_attached_documents',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_other_attached_documents_text',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_program_plans_in_the_future',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_resumes_or_portfolio_of_mentors_coaches_speaker_and_trainers',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_summary_of_the_activities_of_the_program',
            field=files_widget.fields.XFilesField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
