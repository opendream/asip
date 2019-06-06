# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '__first__'),
        ('organization', '0005_auto_20150212_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='organization_type',
            field=models.ForeignKey(related_name='organization_type', blank=True, to='taxonomy.OrganizationType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='client_locations',
            field=models.ManyToManyField(related_name='client_locations', null=True, verbose_name=b'Client Locations', to='taxonomy.Country', blank=True),
            preserve_default=True,
        ),
    ]
