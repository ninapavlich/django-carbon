# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150204_0033'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('page', '0004_menuitem_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='expire_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='hierarchy',
            field=models.CharField(null=True, max_length=255, blank=True, help_text=b'Administrative Hierarchy', unique=True, verbose_name='hierarchy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='path_generated',
            field=models.CharField(help_text=b'The URL path to this page, based on page hierarchy and slug.', max_length=255, null=True, verbose_name='generated path', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='path_override',
            field=models.CharField(help_text=b'The URL path to this page, defined absolutely.', max_length=255, null=True, verbose_name='path override', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='permanent_redirect',
            field=models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='publication_date',
            field=models.DateTimeField(null=True, verbose_name='Publication Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='publication_status',
            field=models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (40, 'Unpublished')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='publish_on_date',
            field=models.DateTimeField(help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='published_by',
            field=models.ForeignKey(related_name='page_menuitem_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='template',
            field=models.ForeignKey(blank=True, to='core.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='temporary_redirect',
            field=models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='uuid',
            field=models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='order',
            field=models.IntegerField(default=0, help_text=b'Simple order of item. '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='parent',
            field=models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='page.MenuItem', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='path',
            field=models.CharField(help_text=b'Actual path used based on generated and override path', max_length=255, null=True, verbose_name='path', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='slug',
            field=models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Slug', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='title',
            field=models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
