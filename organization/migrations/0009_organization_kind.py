# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20160216_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='kind',
            field=models.CharField(default=b'organization', max_length=100, choices=[(b'organization', 'Organization'), (b'product', 'Product/Service')]),
            preserve_default=True,
        ),
    ]
