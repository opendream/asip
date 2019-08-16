# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0040_organizationfundinground'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programstaff',
            name='program',
        ),
        migrations.RemoveField(
            model_name='programstaff',
            name='staff_ptr',
        ),
        migrations.DeleteModel(
            name='ProgramStaff',
        ),
        migrations.RemoveField(
            model_name='program',
            name='attachments',
        ),
        migrations.RemoveField(
            model_name='program',
            name='attachments_types',
        ),
        migrations.RemoveField(
            model_name='program',
            name='changed',
        ),
        migrations.RemoveField(
            model_name='program',
            name='contact_information',
        ),
        migrations.RemoveField(
            model_name='program',
            name='contact_person',
        ),
        migrations.RemoveField(
            model_name='program',
            name='created',
        ),
        migrations.RemoveField(
            model_name='program',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='program',
            name='date_of_establishment',
        ),
        migrations.RemoveField(
            model_name='program',
            name='focus_industry',
        ),
        migrations.RemoveField(
            model_name='program',
            name='focus_sector',
        ),
        migrations.RemoveField(
            model_name='program',
            name='id',
        ),
        migrations.RemoveField(
            model_name='program',
            name='name',
        ),
        migrations.RemoveField(
            model_name='program',
            name='ordering',
        ),
        migrations.RemoveField(
            model_name='program',
            name='other_focus_industry',
        ),
        migrations.RemoveField(
            model_name='program',
            name='other_focus_sector',
        ),
        migrations.RemoveField(
            model_name='program',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='program',
            name='stage_of_participants',
        ),
        migrations.RemoveField(
            model_name='program',
            name='status',
        ),
        migrations.AddField(
            model_name='program',
            name='organization_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='organization.Organization'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='gender_of_representative',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Gender of representative', choices=[(b'M', 'Male'), (b'F', 'Female'), (b'N', 'Prefer not to say')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationstaff',
            name='staff_status',
            field=models.IntegerField(default=1, choices=[(101, 'Mentor'), (100, 'Key Person'), (1, 'Staff')]),
            preserve_default=True,
        ),
    ]
