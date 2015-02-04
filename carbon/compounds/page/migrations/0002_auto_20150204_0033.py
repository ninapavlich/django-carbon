# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_squashed_0012_auto_20150129_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
