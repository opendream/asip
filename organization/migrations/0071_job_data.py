# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    Job = apps.get_model('organization', 'Job')
    JobRole = apps.get_model('taxonomy', 'JobRole')


    role_migrate_map = {
        'administration': 'operations',
        'analyst-scientist': 'data-scientist',
        'designer': 'designer',
        'finance-accounting': 'finance',
        'hardware-engineer': 'hardware-engineer',
        'hr': 'human-resources',
        'legal': 'attorney',
        'management': 'management',
        'marketing-and-pr': 'marketing',
        'operations': 'operations',
        'others': 'other',
        'product-manager': 'product-manager',
        'sales': 'sales',
        'software-engineer': 'developer',
    }

    Location = apps.get_model('taxonomy', 'Location')
    bangkok = Location.objects.get(permalink='bangkok')

    for job in Job.objects.all():
        if job.role:
            job.job_primary_role = JobRole.objects.get(permalink=role_migrate_map[job.role])
            job.save()

        if job.locations.all().count() == 0:
            job.locations.add(bangkok)

def reverse_func(apps, schema_editor):
    pass



class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0011_job_data'),
        ('organization', '0070_auto_20180621_0728'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]