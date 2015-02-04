# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150204_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='file_template',
            field=models.CharField(choices=[(b'403.html', b'403'), (b'404.html', b'404'), (b'500.html', b'500'), (b'base.html', b'Base'), (b'maintenance.html', b'Maintenance'), (b'page/base.html', b'Page - Base'), (b'page/homepage.html', b'Page - Homepage'), (b'partials/footer.html', b'Partials - Footer'), (b'partials/header.html', b'Partials - Header'), (b'partials/item-debug.html', b'Partials - Item Debug'), (b'partials/modernizr.html', b'Partials - Modernizr'), (b'partials/social-sharing.html', b'Partials - Social Sharing'), (b'partials/tracking.html', b'Partials - Tracking')], max_length=255, blank=True, help_text=b'Choose an existing html template file. This will be overwritten in custom template is filled in.', null=True, verbose_name='Template'),
            preserve_default=True,
        ),
    ]
