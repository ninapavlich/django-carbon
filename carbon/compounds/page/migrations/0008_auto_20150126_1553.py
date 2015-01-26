# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0007_template_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='content',
        ),
        migrations.RemoveField(
            model_name='template',
            name='parent',
        ),
        migrations.AddField(
            model_name='template',
            name='custom_template',
            field=models.TextField(default=' ', help_text=b'', verbose_name='custom template'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='template',
            name='slug',
            field=models.CharField(max_length=255, blank=True, help_text=b'', unique=True, verbose_name='Slug', db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='template',
            name='template',
            field=models.CharField(choices=[(b'403.html', b'403'), (b'404.html', b'404'), (b'500.html', b'500'), (b'maintenance.html', b'Maintenance')], max_length=255, blank=True, help_text=b'', null=True, verbose_name='Template'),
            preserve_default=True,
        ),
    ]
