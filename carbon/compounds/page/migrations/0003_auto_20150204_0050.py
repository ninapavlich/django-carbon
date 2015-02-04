# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20150204_0033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='modified_by',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='parent',
            field=models.ForeignKey(blank=True, to='page.MenuItem', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
    ]
