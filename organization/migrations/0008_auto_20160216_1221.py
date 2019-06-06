# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_organizationfunding_organizationgrowthstage_organizationproductlaunch'),
        ('organization', '0007_auto_20160212_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='deal_size_end',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='deal_size_start',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='funding',
            field=models.ForeignKey(related_name='organization_funding', blank=True, to='taxonomy.OrganizationFunding', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='growth_stage',
            field=models.ManyToManyField(related_name='organization_growth_stage', null=True, to='taxonomy.OrganizationGrowthStage', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='product_launch',
            field=models.ForeignKey(related_name='organization_product_launch', blank=True, to='taxonomy.OrganizationProductLaunch', null=True),
            preserve_default=True,
        ),
    ]
