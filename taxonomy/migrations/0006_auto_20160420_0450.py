# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import common.validators
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_investortype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecategory',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='country',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interest',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='investortype',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationfunding',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationgrowthstage',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationproductlaunch',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationrole',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organizationtype',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typeofneed',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typeofsupport',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userrole',
            name='permalink',
            field=models.CharField(help_text='Required unique 30 characters or fewer. Letters, numbers and ./@/+/-/_ characters', unique=True, max_length=255, validators=[common.validators.validate_reserved_url, django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid permalink.', b'invalid')]),
            preserve_default=True,
        ),
    ]
