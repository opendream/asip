# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0010_jobrole_location'),
        ('account', '0005_user_notification_allow_email_send_organization_organizationparticipate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job_criteria',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_locations',
            field=models.ManyToManyField(to='taxonomy.Location', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_position',
            field=models.CharField(blank=True, max_length=128, null=True, choices=[(b'full-time', 'Full-time Employee'), (b'contract', 'Contractor'), (b'internship', 'Intern'), (b'cofounder', 'Co-founder')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_primary_role',
            field=models.ForeignKey(related_name='user_job_primary_role', blank=True, to='taxonomy.JobRole', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_remote',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_roles',
            field=models.ManyToManyField(related_name='user_job_roles', null=True, to='taxonomy.JobRole', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job_status',
            field=models.CharField(blank=True, max_length=128, null=True, choices=[(b'starting', b'Starting to look'), (b'actively', b'Actively interviewing'), (b'open', b'Open to offers'), (b'closed', b'Closed to offers')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='money_salary',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, blank=True, null=True, default_currency=b'THB'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='money_salary_currency',
            field=djmoney.models.fields.CurrencyField(default=b'THB', max_length=3, editable=False, choices=[(b'THB', b'THB'), (b'USD', b'USD')]),
            preserve_default=True,
        ),
    ]
