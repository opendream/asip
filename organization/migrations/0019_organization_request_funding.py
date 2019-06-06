# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_investortype'),
        ('organization', '0018_auto_20160418_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='request_funding',
            field=models.ForeignKey(related_name='organization_request_funding', blank=True, to='taxonomy.OrganizationFunding', null=True),
            preserve_default=True,
        ),
    ]
