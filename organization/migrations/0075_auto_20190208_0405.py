# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0074_auto_20180704_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='attachments_biography_consisting_of_major_achievements_of_management_levels',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Minimum 5 biography consisting of major achievements (if any) of management levels', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_financial_statement',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Financial Statement', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_incorporation_registration_certificate',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Incorporation/Registration Certificate', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_investment_portfolio',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Investment Portfolio', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_list_of_notable_startup_team_alumni',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'List of notable startup/team alumni', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_list_of_organization_or_program_partners',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'List of organization or program partners', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_list_of_organizational_or_program_partners',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'List of organizational or program partners (if any)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_long_term_sustainable_revenue_model',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Long-term sustainable revenue model', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_other_attached_documents',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_other_attached_documents_text',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Other attached documents, Please specify', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_program_plans_in_the_future',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Program plans in the future', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_resumes_or_portfolio_of_mentors_coaches_speaker_and_trainers',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Minimum 5 resumes or portfolio(consisting of previous achievement) of mentors, coaches, speaker, and trainers', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='attachments_summary_of_the_activities_of_the_program',
            field=files_widget.fields.XFilesField(null=True, verbose_name=b'Summary of the activities of the program', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_register_to_nia',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
