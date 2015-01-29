# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0009_auto_20150126_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='custom_template',
            field=models.TextField(help_text=b'Override html template file with a custom template.', null=True, verbose_name='custom template', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='slug',
            field=models.CharField(max_length=255, blank=True, help_text=b'This slug can be referenced within templates: {% extends template-slug %}', unique=True, verbose_name='Slug', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='template',
            name='template',
            field=models.CharField(choices=[(b'403.html', b'403'), (b'404.html', b'404'), (b'500.html', b'500'), (b'maintenance.html', b'Maintenance'), (b'test.html', b'Test')], max_length=255, blank=True, help_text=b'Choose an existing html template file. This will be overwritten in custom template is filled in.', null=True, verbose_name='Template'),
            preserve_default=True,
        ),
    ]
