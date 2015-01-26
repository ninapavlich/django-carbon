# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20150120_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcategory',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectmedia',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
