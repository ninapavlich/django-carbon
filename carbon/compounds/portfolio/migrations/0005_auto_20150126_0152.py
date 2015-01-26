# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_auto_20150126_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmedia',
            name='use_png',
        ),
        migrations.AlterField(
            model_name='projectmedia',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', null=True),
            preserve_default=True,
        ),
    ]
