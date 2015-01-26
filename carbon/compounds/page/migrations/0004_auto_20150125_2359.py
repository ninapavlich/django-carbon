# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_auto_20150125_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pagetag',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
