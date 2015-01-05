# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atoms', '__first__'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('seoatom_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='atoms.SEOAtom')),
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
                ('sharable', models.BooleanField(default=False, help_text=b'Is URL a sharable URL')),
                ('tiny_url', models.CharField(help_text=b'Tiny URL used for social sharing', unique=True, max_length=255, verbose_name='tiny url')),
                ('social_share_type', models.CharField(default=b'article', choices=[(b'article', b'Article'), (b'book', b'Book'), (b'profile', b'Profile'), (b'website', b'Website'), (b'video.movie', b'Video - Movie'), (b'video.episode', b'Video - Episode'), (b'video.tv_show', b'Video - TV Show'), (b'video.other', b'Video - Other'), (b'music.song', b'Music - Song'), (b'music.album', b'Music - Album'), (b'music.radio_station', b'Music - Playlist'), (b'music.radio_station', b'Music - Radio Station')], max_length=255, blank=True, null=True, verbose_name=b'Social type')),
                ('facebook_author_id', models.CharField(help_text=b'Numeric Facebook ID', max_length=255, null=True, verbose_name=b'Facebook Author ID', blank=True)),
                ('twitter_author_id', models.CharField(help_text=b'Twitter handle, including "@" e.g. @cgpartners', max_length=255, null=True, verbose_name=b'Twitter Admin ID', blank=True)),
                ('google_author_id', models.CharField(help_text=b'Google author id, e.g. the AUTHOR_ID in https://plus.google.com/AUTHOR_ID/posts', max_length=255, null=True, verbose_name=b'Google Admin ID', blank=True)),
                ('content', models.TextField(help_text=b'Allow item to be shared on social networks', verbose_name='content')),
                ('allow_comments', models.BooleanField(default=False, help_text=b'')),
                ('authors', models.ManyToManyField(help_text=b'', related_name='blog_article_authors', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('atoms.seoatom', models.Model),
        ),
        migrations.CreateModel(
            name='Category',
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
                ('created_by', models.ForeignKey(related_name='blog_category_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('groups_blacklist', models.ManyToManyField(related_name='blog_category_blacklist_groups', null=True, to='auth.Group', blank=True)),
                ('groups_whitelist', models.ManyToManyField(related_name='blog_category_whitelist_groups', null=True, to='auth.Group', blank=True)),
                ('modified_by', models.ForeignKey(related_name='blog_category_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='blog.Category', null=True)),
                ('published_by', models.ForeignKey(related_name='blog_category_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_blacklist', models.ManyToManyField(related_name='blog_category_blacklist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('user_whitelist', models.ManyToManyField(related_name='blog_category_whitelist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
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
                ('created_by', models.ForeignKey(related_name='blog_tag_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('groups_blacklist', models.ManyToManyField(related_name='blog_tag_blacklist_groups', null=True, to='auth.Group', blank=True)),
                ('groups_whitelist', models.ManyToManyField(related_name='blog_tag_whitelist_groups', null=True, to='auth.Group', blank=True)),
                ('modified_by', models.ForeignKey(related_name='blog_tag_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('published_by', models.ForeignKey(related_name='blog_tag_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_blacklist', models.ManyToManyField(related_name='blog_tag_blacklist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('user_whitelist', models.ManyToManyField(related_name='blog_tag_whitelist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='blog.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='created_by',
            field=models.ForeignKey(related_name='blog_article_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='editors',
            field=models.ManyToManyField(help_text=b'', related_name='blog_article_editors', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='groups_blacklist',
            field=models.ManyToManyField(related_name='blog_article_blacklist_groups', null=True, to='auth.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='groups_whitelist',
            field=models.ManyToManyField(related_name='blog_article_whitelist_groups', null=True, to='auth.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ForeignKey(related_name='blog_article_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Featured image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='modified_by',
            field=models.ForeignKey(related_name='blog_article_modified_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='parent',
            field=models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='blog.Article', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='published_by',
            field=models.ForeignKey(related_name='blog_article_published_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='social_share_image',
            field=models.ForeignKey(related_name='blog_article_social_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Standards for the social share image vary, but an image at least 300x200px should work well.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='user_blacklist',
            field=models.ManyToManyField(related_name='blog_article_blacklist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='user_whitelist',
            field=models.ManyToManyField(related_name='blog_article_whitelist_user', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
