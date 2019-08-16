# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0043_auto_20180502_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='phone_number_of_contact_person',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='store_email_of_organizations_headquarters',
            field=models.EmailField(max_length=255, null=True, verbose_name='Email of Organization', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='title_of_contact_person',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
