# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20150429_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='images',
            field=files_widget.fields.ImagesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='type_of_organization',
            field=models.CharField(default=b'startup', max_length=128, choices=[(b'social-enterprise', 'Social Enterprise'), (b'startup', 'Startup'), (b'supporter', 'Supporters/Investors')]),
            preserve_default=True,
        ),
    ]
