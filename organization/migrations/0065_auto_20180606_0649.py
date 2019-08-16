# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0064_organization_other_attachments_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationparticipate',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='organizationparticipate',
            name='program',
        ),
        migrations.DeleteModel(
            name='OrganizationParticipate',
        ),
    ]
