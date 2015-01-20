# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, verbose_name='Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Slug', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'Actual path used based on generated and override path', max_length=255, null=True, verbose_name='path', blank=True)),
                ('path_generated', models.CharField(help_text=b'The URL path to this page, based on page hierarchy and slug.', max_length=255, null=True, verbose_name='generated path', blank=True)),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', max_length=255, null=True, verbose_name='path override', blank=True)),
                ('hierarchy', models.CharField(null=True, max_length=255, blank=True, help_text=b'Administrative Hierarchy', unique=True, verbose_name='hierarchy')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('publication_date', models.DateTimeField(null=True, verbose_name='Publication Date', blank=True)),
                ('publication_status', models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (30, 'Expired'), (40, 'Unpublished')])),
                ('page_meta_description', models.CharField(help_text=b'A short description of the page, used for SEO and not displayed to the user.', max_length=2000, verbose_name='Meta Description', blank=True)),
                ('page_meta_keywords', models.CharField(help_text=b'A short list of keywords of the page, used for SEO and not displayed to the user.', max_length=2000, verbose_name='Meta Page Keywords', blank=True)),
                ('is_searchable', models.BooleanField(default=True, help_text=b'Allow search engines to index this object and display in sitemap.')),
                ('in_sitemap', models.BooleanField(default=True, help_text=b'Is in sitemap')),
                ('noindex', models.BooleanField(default=False, help_text=b'Robots noindex')),
                ('nofollow', models.BooleanField(default=False, help_text=b'Robots nofollow')),
                ('sitemap_changefreq', models.CharField(default=b'monthly', help_text=b'How frequently does page content update', max_length=255, verbose_name='Sitemap Change Frequency', choices=[(b'never', 'Never'), (b'yearly', 'Yearly'), (b'monthly', 'Monthly'), (b'weekly', 'Weekly'), (b'daily', 'Daily'), (b'hourly', 'Hourly'), (b'always', 'Always')])),
                ('sitemap_priority', models.CharField(default=b'0.5', max_length=255, blank=True, help_text=b'Sitemap priority', null=True, verbose_name=b'Sitemap Priority')),
                ('sharable', models.BooleanField(default=False, help_text=b'Is URL a sharable URL')),
                ('tiny_url', models.CharField(help_text=b'Tiny URL used for social sharing', max_length=255, null=True, verbose_name='tiny url', blank=True)),
                ('social_share_type', models.CharField(default=b'article', choices=[(b'article', b'Article'), (b'book', b'Book'), (b'profile', b'Profile'), (b'website', b'Website'), (b'video.movie', b'Video - Movie'), (b'video.episode', b'Video - Episode'), (b'video.tv_show', b'Video - TV Show'), (b'video.other', b'Video - Other'), (b'music.song', b'Music - Song'), (b'music.album', b'Music - Album'), (b'music.radio_station', b'Music - Playlist'), (b'music.radio_station', b'Music - Radio Station')], max_length=255, blank=True, null=True, verbose_name=b'Social type')),
                ('facebook_author_id', models.CharField(help_text=b'Numeric Facebook ID', max_length=255, null=True, verbose_name=b'Facebook Author ID', blank=True)),
                ('twitter_author_id', models.CharField(help_text=b'Twitter handle, including "@" e.g. @cgpartners', max_length=255, null=True, verbose_name=b'Twitter Admin ID', blank=True)),
                ('google_author_id', models.CharField(help_text=b'Google author id, e.g. the AUTHOR_ID in https://plus.google.com/AUTHOR_ID/posts', max_length=255, null=True, verbose_name=b'Google Admin ID', blank=True)),
                ('content', models.TextField(help_text=b'', null=True, verbose_name='content', blank=True)),
                ('allow_comments', models.BooleanField(default=False, help_text=b'')),
                ('authors', models.ManyToManyField(help_text=b'', related_name='page_page_authors', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('created_by', models.ForeignKey(related_name='page_page_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('editors', models.ManyToManyField(help_text=b'', related_name='page_page_editors', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('image', models.ForeignKey(related_name='page_page_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Featured image', null=True)),
                ('modified_by', models.ForeignKey(related_name='page_page_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='page.Page', null=True)),
                ('published_by', models.ForeignKey(related_name='page_page_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('social_share_image', models.ForeignKey(related_name='page_page_social_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Standards for the social share image vary, but an image at least 300x200px should work well.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'The display title for this object.', max_length=255, verbose_name='Title')),
                ('slug', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='Slug', db_index=True)),
                ('uuid', models.CharField(max_length=255, blank=True, help_text=b'Auto-generated page slug for this object.', unique=True, verbose_name='UUID', db_index=True)),
                ('order', models.IntegerField(default=0, help_text=b'Simple order of item. ')),
                ('path', models.CharField(help_text=b'Actual path used based on generated and override path', max_length=255, null=True, verbose_name='path', blank=True)),
                ('path_generated', models.CharField(help_text=b'The URL path to this page, based on page hierarchy and slug.', max_length=255, null=True, verbose_name='generated path', blank=True)),
                ('path_override', models.CharField(help_text=b'The URL path to this page, defined absolutely.', max_length=255, null=True, verbose_name='path override', blank=True)),
                ('hierarchy', models.CharField(null=True, max_length=255, blank=True, help_text=b'Administrative Hierarchy', unique=True, verbose_name='hierarchy')),
                ('temporary_redirect', models.CharField(help_text=b'Temporarily redirect to a different path', max_length=255, verbose_name='Temporary Redirect', blank=True)),
                ('permanent_redirect', models.CharField(help_text=b'Permanently redirect to a different path', max_length=255, verbose_name='Permanent Redirect', blank=True)),
                ('publication_date', models.DateTimeField(null=True, verbose_name='Publication Date', blank=True)),
                ('publication_status', models.IntegerField(default=10, help_text=b'Current publication status', choices=[(10, 'Draft'), (20, 'Needs Review'), (100, 'Published'), (30, 'Expired'), (40, 'Unpublished')])),
                ('created_by', models.ForeignKey(related_name='page_pagecategory_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='page_pagecategory_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='page.PageCategory', null=True)),
                ('published_by', models.ForeignKey(related_name='page_pagecategory_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageCategoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('order', models.IntegerField(default=0, help_text=b'')),
                ('category', models.ForeignKey(to='page.PageCategory')),
                ('created_by', models.ForeignKey(related_name='page_pagecategoryitem_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('item', models.ForeignKey(to='page.Page')),
                ('modified_by', models.ForeignKey(related_name='page_pagecategoryitem_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date', null=True)),
                ('admin_note', models.TextField(null=True, verbose_name='admin note', blank=True)),
                ('title', models.CharField(help_text=b'', max_length=255, verbose_name='Page Title')),
                ('content', models.TextField(help_text=b'Allow item to be shared on social networks', verbose_name='content')),
                ('created_by', models.ForeignKey(related_name='page_template_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='page_template_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
