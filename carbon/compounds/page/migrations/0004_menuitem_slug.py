# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_auto_20150204_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='slug',
            field=models.CharField(max_length=255, blank=True, help_text=b'', unique=True, verbose_name='Slug', db_index=True),
            preserve_default=True,
        ),
    ]
