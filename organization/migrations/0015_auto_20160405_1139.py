# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_investortype'),
        ('organization', '0014_organization_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='investor_types',
            field=models.ManyToManyField(related_name='investor_types', null=True, to='taxonomy.InvestorType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='organization_types',
            field=models.ManyToManyField(related_name='organization_types', null=True, to='taxonomy.OrganizationType', blank=True),
            preserve_default=True,
        ),
    ]
