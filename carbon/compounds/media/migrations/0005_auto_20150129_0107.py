# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('global', '__first__'),
        ('media', '0004_auto_20150126_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='media',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='secureimage',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='securemedia',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
    ]
