# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientset', '0004_auto_20150126_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientmedia',
            name='use_png',
        ),
        migrations.AlterField(
            model_name='clientmedia',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', null=True),
            preserve_default=True,
        ),
    ]
