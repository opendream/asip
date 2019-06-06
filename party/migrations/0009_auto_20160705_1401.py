# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Party = apps.get_model("party", "Party")
    for party in Party.objects.filter(special__isnull=False):
        party.specials.add(party.special)


class Migration(migrations.Migration):

    dependencies = [
        ('special', '0002_special_image'),
        ('party', '0008_auto_20160526_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='specials',
            field=models.ManyToManyField(related_name='specials_party_list', null=True, to='special.Special', blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(forwards_func),
    ]
