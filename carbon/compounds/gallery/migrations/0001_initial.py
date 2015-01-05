# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import carbon.atoms.models.media
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
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
                ('require_registered_user', models.BooleanField(default=False, help_text=b'Require logged in user', verbose_name='Required Registered Users')),
                ('password', models.CharField(help_text=b'Password to use if access_restriction is set to Password', max_length=255, null=True, verbose_name='Encrypted Password', blank=True)),
                ('publish_on_date', models.DateTimeField(auto_now=True, help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date')),
                ('expire_on_date', models.DateTimeField(auto_now=True, help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date')),
                ('publication_date', models.DateTimeField(auto_now=True, verbose_name='Publication Date', null=True)),
                ('publication_status', models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (30, 'Expired'), (40, 'Unpublished')])),
                ('created_by', models.ForeignKey(related_name='gallery_client_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('groups_blacklist', models.ManyToManyField(related_name='gallery_client_blacklist_groups', null=True, to='auth.Group', blank=True)),
                ('groups_whitelist', models.ManyToManyField(related_name='gallery_client_whitelist_groups', null=True, to='auth.Group', blank=True)),
                ('modified_by', models.ForeignKey(related_name='gallery_client_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('published_by', models.ForeignKey(related_name='gallery_client_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_blacklist', models.ManyToManyField(related_name='gallery_client_blacklist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('user_whitelist', models.ManyToManyField(related_name='gallery_client_whitelist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientImage',
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
                ('created_by', models.ForeignKey(related_name='gallery_clientimage_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='gallery_clientimage_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientImageSet',
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
                ('require_registered_user', models.BooleanField(default=False, help_text=b'Require logged in user', verbose_name='Required Registered Users')),
                ('password', models.CharField(help_text=b'Password to use if access_restriction is set to Password', max_length=255, null=True, verbose_name='Encrypted Password', blank=True)),
                ('publish_on_date', models.DateTimeField(auto_now=True, help_text=b"Object state will be set to 'Published' on this date.", null=True, verbose_name='Publish on Date')),
                ('expire_on_date', models.DateTimeField(auto_now=True, help_text=b"Object state will be set to 'Expired' on this date.", null=True, verbose_name='Expire on Date')),
                ('publication_date', models.DateTimeField(auto_now=True, verbose_name='Publication Date', null=True)),
                ('publication_status', models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (30, 'Expired'), (40, 'Unpublished')])),
                ('client', models.ForeignKey(blank=True, to='gallery.Client', null=True)),
                ('created_by', models.ForeignKey(related_name='gallery_clientimageset_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('groups_blacklist', models.ManyToManyField(related_name='gallery_clientimageset_blacklist_groups', null=True, to='auth.Group', blank=True)),
                ('groups_whitelist', models.ManyToManyField(related_name='gallery_clientimageset_whitelist_groups', null=True, to='auth.Group', blank=True)),
                ('modified_by', models.ForeignKey(related_name='gallery_clientimageset_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='gallery.ClientImageSet', null=True)),
                ('published_by', models.ForeignKey(related_name='gallery_clientimageset_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_blacklist', models.ManyToManyField(related_name='gallery_clientimageset_blacklist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('user_whitelist', models.ManyToManyField(related_name='gallery_clientimageset_whitelist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
