# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_auto_20150126_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(to='page.PageTag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.ForeignKey(blank=True, to='page.Template', null=True),
            preserve_default=True,
        ),
    ]
