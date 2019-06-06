# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators
import common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0019_organization_request_funding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
    ]
