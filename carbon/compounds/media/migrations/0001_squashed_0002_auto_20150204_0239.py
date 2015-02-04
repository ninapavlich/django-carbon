# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import carbon.atoms.models.media
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    # replaces = [(b'media', '0001_squashed_0007_auto_20150204_0236'), (b'media', '0002_auto_20150204_0239')]

    dependencies = [
        ('global', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atoms', '__first__'),
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
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Slug', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'Actual path used based on generated and override path', max_length=255, null=True, verbose_name='path', blank=True)),
                ('path_generated', models.CharField(help_text=b'The URL path to this page, based on page hierarchy and slug.', max_length=255, null=True, verbose_name='generated path', blank=True)),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', max_length=255, null=True, verbose_name='path override', blank=True)),
                ('hierarchy', models.CharField(null=True, max_length=255, blank=True, help_text=b'Administrative Hierarchy', unique=True, verbose_name='hierarchy')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('image', models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('use_png', models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)')),
                ('created_by', models.ForeignKey(related_name='media_image_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='media_image_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('allow_overwrite', models.BooleanField(default=False, help_text=b"Allow file to write over an existing file if the name             is the same. If not, we'll automatically add a numerical suffix to             ensure file doesn't override existing files.", verbose_name='Allow Overwrite')),
                ('template', models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True)),
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
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Slug', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'Actual path used based on generated and override path', max_length=255, null=True, verbose_name='path', blank=True)),
                ('path_generated', models.CharField(help_text=b'The URL path to this page, based on page hierarchy and slug.', max_length=255, null=True, verbose_name='generated path', blank=True)),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', max_length=255, null=True, verbose_name='path override', blank=True)),
                ('hierarchy', models.CharField(null=True, max_length=255, blank=True, help_text=b'Administrative Hierarchy', unique=True, verbose_name='hierarchy')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Item credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Item caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('image', models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('use_png', models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)')),
                ('file', models.FileField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('created_by', models.ForeignKey(related_name='media_media_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
                ('secureimagemolecule_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='atoms.SecureImageMolecule')),
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
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, null=True, verbose_name='Title', blank=True)),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Slug', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'Actual path used based on generated and override path', max_length=255, null=True, verbose_name='path', blank=True)),
                ('path_generated', models.CharField(help_text=b'The URL path to this page, based on page hierarchy and slug.', max_length=255, null=True, verbose_name='generated path', blank=True)),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', max_length=255, null=True, verbose_name='path override', blank=True)),
                ('hierarchy', models.CharField(null=True, max_length=255, blank=True, help_text=b'Administrative Hierarchy', unique=True, verbose_name='hierarchy')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('credit', models.CharField(help_text=b'Item credit', max_length=255, verbose_name='Credit', blank=True)),
                ('caption', models.TextField(help_text=b'Item caption', verbose_name='Caption', blank=True)),
                ('alt', models.CharField(help_text=b'Alt text', max_length=255, verbose_name='Alt Text', blank=True)),
                ('clean_filename_on_upload', models.BooleanField(default=True, help_text=b'Clean the filename on upload', verbose_name='Clean filename on upload')),
                ('image', models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('use_png', models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)')),
                ('file', models.FileField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True)),
                ('created_by', models.ForeignKey(related_name='media_securemedia_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='media_securemedia_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'media'},
        ),
        migrations.AlterModelOptions(
            name='securemedia',
            options={'verbose_name_plural': 'secure media'},
        ),
        migrations.AddField(
            model_name='media',
            name='allow_overwrite',
            field=models.BooleanField(default=False, help_text=b"Allow file to write over an existing file if the name             is the same. If not, we'll automatically add a numerical suffix to             ensure file doesn't override existing files.", verbose_name='Allow Overwrite'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='media',
            name='use_png',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='use_png',
        ),
        migrations.AlterField(
            model_name='media',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='image',
        ),
        migrations.AddField(
            model_name='media',
            name='template',
            field=models.ForeignKey(blank=True, to='global.Template', help_text=b'Template for view', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='admin_note',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='alt',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='clean_filename_on_upload',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='hierarchy',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='id',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='order',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='path',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='path_generated',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='path_override',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='permanent_redirect',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='temporary_redirect',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='title',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='securemedia',
            name='version',
        ),
        migrations.AddField(
            model_name='media',
            name='use_png',
            field=models.BooleanField(default=False, verbose_name=b'Use .PNG (instead of .JPG)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='securemedia',
            name='secureimagemolecule_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='atoms.SecureImageMolecule'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='media',
            name='image',
            field=models.ImageField(null=True, upload_to=carbon.atoms.models.media.title_file_name, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='media',
            name='caption',
            field=models.TextField(help_text=b'Caption', verbose_name='Caption', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='media',
            name='credit',
            field=models.CharField(help_text=b'Credit', max_length=255, verbose_name='Credit', blank=True),
            preserve_default=True,
        ),
    ]
