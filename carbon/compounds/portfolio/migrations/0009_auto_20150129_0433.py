# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import carbon.atoms.models.media


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_auto_20150129_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmedia',
            name='use_png',
            field=models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectmedia',
            name='image',
            field=models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True),
            preserve_default=True,
        ),
    ]
