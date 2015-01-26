# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_auto_20150126_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcategory',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcategory',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
    ]
