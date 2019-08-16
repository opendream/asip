# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import files_widget.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_programtype_typeofassistantship_typeofattachment_typeofbatch_typeoffinancialsource_typeoffocusindust'),
        ('organization', '0034_auto_20180424_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='attachments',
            field=files_widget.fields.FilesField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='attachments_types',
            field=models.ManyToManyField(related_name='orgazation_attachments_types', null=True, to='taxonomy.TypeOfAttachment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='financial_source',
            field=models.ManyToManyField(related_name='organization_financial_source', null=True, to='taxonomy.TypeOfFinancialSource', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='other_financial_source',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
