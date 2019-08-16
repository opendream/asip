# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20180703_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Required 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=255, verbose_name='username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), 'Enter a valid username.', b'invalid')]),
            preserve_default=True,
        ),
    ]
