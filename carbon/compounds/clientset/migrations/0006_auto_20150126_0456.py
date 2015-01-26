# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientset', '0005_auto_20150126_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsetcategory',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
    ]
