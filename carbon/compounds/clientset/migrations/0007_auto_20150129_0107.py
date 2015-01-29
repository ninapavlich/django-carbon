# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('global', '__first__'),
        ('clientset', '0006_auto_20150126_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientmedia',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
    ]
