# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0027_program_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProgramStaff',
        ),
    ]
