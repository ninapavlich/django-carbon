# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20150125_2359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'media'},
        ),
        migrations.AlterModelOptions(
            name='securemedia',
            options={'verbose_name_plural': 'secure media'},
        ),
        migrations.AddField(
            model_name='image',
            name='allow_overwrite',
            field=models.BooleanField(default=False, help_text=b"Allow file to write over an existing file if the name             is the same. If not, we'll automatically add a numerical suffix to             ensure file doesn't override existing files.", verbose_name='Allow Overwrite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='media',
            name='allow_overwrite',
            field=models.BooleanField(default=False, help_text=b"Allow file to write over an existing file if the name             is the same. If not, we'll automatically add a numerical suffix to             ensure file doesn't override existing files.", verbose_name='Allow Overwrite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='secureimage',
            name='allow_overwrite',
            field=models.BooleanField(default=False, help_text=b"Allow file to write over an existing file if the name             is the same. If not, we'll automatically add a numerical suffix to             ensure file doesn't override existing files.", verbose_name='Allow Overwrite'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='securemedia',
            name='allow_overwrite',
            field=models.BooleanField(default=False, help_text=b"Allow file to write over an existing file if the name             is the same. If not, we'll automatically add a numerical suffix to             ensure file doesn't override existing files.", verbose_name='Allow Overwrite'),
            preserve_default=True,
        ),
    ]
