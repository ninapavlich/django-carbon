# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0008_auto_20150126_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='custom_template',
            field=models.TextField(help_text=b'', null=True, verbose_name='custom template', blank=True),
            preserve_default=True,
        ),
    ]
