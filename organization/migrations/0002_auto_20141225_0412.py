# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '__first__'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='organization_primary_role',
            field=models.ForeignKey(related_name='primary_organization_role', blank=True, to='taxonomy.OrganizationRole', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='organization_roles',
            field=models.ManyToManyField(related_name='organization_roles', null=True, to='taxonomy.OrganizationRole', blank=True),
            preserve_default=True,
        ),
    ]
