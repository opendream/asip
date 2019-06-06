# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_many_types(apps, schema_editor):
    """
        Adds the Author object in Book.author to the
        many-to-many relationship in Book.authors
    """
    Organization = apps.get_model('organization', 'Organization')

    for organization in Organization.objects.all():
        if organization.organization_type:
            organization.organization_types.add(organization.organization_type)
        if organization.investor_type:
            organization.investor_types.add(organization.investor_type)

class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0015_auto_20160405_1139'),
    ]

    operations = [
        migrations.RunPython(make_many_types),
    ]
