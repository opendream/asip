# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_programtype_typeofassistantship_typeofattachment_typeofbatch_typeoffinancialsource_typeoffocusindust'),
        ('organization', '0032_auto_20180420_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationAssistance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('assistance', models.ForeignKey(related_name='organization_assistance', to='taxonomy.TypeOfAssistantship')),
                ('organization', models.ForeignKey(related_name='assistance_organization', to='organization.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationStaff',
            fields=[
                ('staff_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='organization.Staff')),
                ('priority', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveIntegerField(null=True, blank=True)),
                ('staff_status', models.IntegerField(default=1, choices=[(100, 'Key Person'), (1, 'Staff')])),
                ('organization', models.ForeignKey(related_name='staff_organization', to='organization.Organization')),
            ],
            options={
                'abstract': False,
            },
            bases=('organization.staff', models.Model),
        ),
        migrations.AddField(
            model_name='organization',
            name='amount_of_money_invested',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='business_model',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='company_mission',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='company_registration_number',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='company_vision',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='extra_information',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='growth_strategy',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='has_participate_in_program',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='has_received_investment',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='has_taken_equity_in_fund_organization',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='is_lead_investor',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='is_register_to_nia',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='money_raise',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='participate_program',
            field=models.ManyToManyField(related_name='organization_programs', null=True, to='organization.Program', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='pre_money_valuation',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='specialty',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='target_funding',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
