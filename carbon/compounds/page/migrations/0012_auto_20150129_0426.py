# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_auto_20150129_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='publication_status',
            field=models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (40, 'Unpublished')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pagetag',
            name='publication_status',
            field=models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (40, 'Unpublished')]),
            preserve_default=True,
        ),
    ]
