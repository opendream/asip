# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    CommonCms = apps.get_model("cms", "CommonCms")
    for cms in CommonCms.objects.all():
        cms.party_created_by = cms.created_by.party_ptr
        cms.save()

        cms = CommonCms.objects.get(id=cms.id)
        print cms.party_created_by

def reverse_func(apps, schema_editor):
    CommonCms = apps.get_model("cms", "CommonCms")
    for cms in CommonCms.objects.all():
        cms.party_created_by = None
        cms.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20160210_0335'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
        # migrations.AlterField(
        #     model_name='commoncms',
        #     name='party_created_by',
        #     field=models.ForeignKey(related_name='cms_party_created_by', to='party.Party'),
        #     preserve_default=True,
        # ),
    ]