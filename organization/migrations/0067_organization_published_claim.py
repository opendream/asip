# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0066_organization_claim_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='published_claim',
            field=models.ForeignKey(related_name='published_claim_organization', blank=True, to='organization.Organization', null=True),
            preserve_default=True,
        ),
    ]
