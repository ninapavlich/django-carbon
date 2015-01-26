# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_menu_menuitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='path',
            field=models.CharField(help_text=b'Override path for this menu item', max_length=255, null=True, verbose_name='Path', blank=True),
            preserve_default=True,
        ),
    ]
