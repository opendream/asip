# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_organization_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='kind',
            field=models.CharField(default=b'organization', max_length=100, choices=[(b'product', 'Product/Service'), (b'organization', 'Organization')]),
            preserve_default=True,
        ),
    ]
