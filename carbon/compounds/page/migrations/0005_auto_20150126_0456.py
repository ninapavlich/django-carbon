# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_auto_20150125_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagetag',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagetag',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
    ]
