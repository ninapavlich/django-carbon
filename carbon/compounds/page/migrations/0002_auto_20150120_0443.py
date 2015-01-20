# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(default=1, to='page.Template'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='template',
            name='content',
            field=models.TextField(help_text=b'', verbose_name='content'),
            preserve_default=True,
        ),
    ]
