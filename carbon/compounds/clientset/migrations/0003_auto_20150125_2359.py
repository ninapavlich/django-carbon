# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientset', '0002_auto_20150120_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientmedia',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientsetcategory',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
