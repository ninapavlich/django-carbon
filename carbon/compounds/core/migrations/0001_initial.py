# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'', max_length=255, verbose_name='Page Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'This slug can be referenced within templates: {% extends template-slug %}', unique=True, verbose_name='Slug', db_index=True)),
                ('custom_template', models.TextField(help_text=b'Override html template file with a custom template.', null=True, verbose_name='custom template', blank=True)),
                ('file_template', models.CharField(choices=[(b'403.html', b'403'), (b'404.html', b'404'), (b'500.html', b'500'), (b'base.html', b'Base'), (b'maintenance.html', b'Maintenance'), (b'page/base.html', b'Page - Base'), (b'partials/footer.html', b'Partials - Footer'), (b'partials/header.html', b'Partials - Header'), (b'partials/item-debug.html', b'Partials - Item Debug'), (b'partials/modernizr.html', b'Partials - Modernizr'), (b'partials/tracking.html', b'Partials - Tracking')], max_length=255, blank=True, help_text=b'Choose an existing html template file. This will be overwritten in custom template is filled in.', null=True, verbose_name='Template')),
                ('created_by', models.ForeignKey(related_name='core_template_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='core_template_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
