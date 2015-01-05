# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import carbon.atoms.models.media
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, verbose_name='Page Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Text ID', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'The URL path to this page, based on page heirarchy and slug.', unique=True, max_length=255, verbose_name='path')),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', unique=True, max_length=255, verbose_name='path override')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Item credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Item caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('image', models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('use_png', models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)')),
                ('created_by', models.ForeignKey(related_name='media_image_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='media_image_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, verbose_name='Page Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Text ID', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'The URL path to this page, based on page heirarchy and slug.', unique=True, max_length=255, verbose_name='path')),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', unique=True, max_length=255, verbose_name='path override')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Item credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Item caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('file', models.FileField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('created_by', models.ForeignKey(related_name='media_media_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('image', models.ForeignKey(related_name='media_media_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Featured image', null=True)),
                ('modified_by', models.ForeignKey(related_name='media_media_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecureImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, verbose_name='Page Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Text ID', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'The URL path to this page, based on page heirarchy and slug.', unique=True, max_length=255, verbose_name='path')),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', unique=True, max_length=255, verbose_name='path override')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Item credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Item caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('image', models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('use_png', models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)')),
                ('created_by', models.ForeignKey(related_name='media_secureimage_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='media_secureimage_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecureMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, verbose_name='Page Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Text ID', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'The URL path to this page, based on page heirarchy and slug.', unique=True, max_length=255, verbose_name='path')),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', unique=True, max_length=255, verbose_name='path override')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Item credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Item caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('file', models.FileField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('created_by', models.ForeignKey(related_name='media_securemedia_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('image', models.ForeignKey(related_name='media_securemedia_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Featured image', null=True)),
                ('modified_by', models.ForeignKey(related_name='media_securemedia_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
