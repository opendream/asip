# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0004_articlecategory'),
        ('cms', '0012_auto_20160315_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='categories',
            field=models.ManyToManyField(related_name='cms_categories', null=True, to='taxonomy.ArticleCategory', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='article_category',
            field=models.CharField(default=b'news', max_length=255, choices=[(b'news', 'News'), (b'knowledge-tools', 'Knowledge & Tools')]),
            preserve_default=True,
        ),
    ]
