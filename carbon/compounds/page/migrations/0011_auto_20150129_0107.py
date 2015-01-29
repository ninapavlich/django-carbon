# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('global', '__first__'),
        ('page', '0010_auto_20150128_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='template',
            name='modified_by',
        ),
        migrations.AddField(
            model_name='pagetag',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Template',
        ),
    ]
