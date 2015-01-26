# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='media',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='secureimage',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='securemedia',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
