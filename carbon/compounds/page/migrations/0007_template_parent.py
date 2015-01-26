# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0006_auto_20150126_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='parent',
            field=models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='page.Template', null=True),
            preserve_default=True,
        ),
    ]
