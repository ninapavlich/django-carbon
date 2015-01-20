# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
        ('clientset', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsetcategory',
            name='facebook_author_id',
            field=models.CharField(help_text=b'Numeric Facebook ID', max_length=255, null=True, verbose_name=b'Facebook Author ID', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='google_author_id',
            field=models.CharField(help_text=b'Google author id, e.g. the AUTHOR_ID in https://plus.google.com/AUTHOR_ID/posts', max_length=255, null=True, verbose_name=b'Google Admin ID', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='in_sitemap',
            field=models.BooleanField(default=True, help_text=b'Is in sitemap'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='is_searchable',
            field=models.BooleanField(default=True, help_text=b'Allow search engines to index this object and display in sitemap.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='nofollow',
            field=models.BooleanField(default=False, help_text=b'Robots nofollow'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='noindex',
            field=models.BooleanField(default=False, help_text=b'Robots noindex'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='page_meta_description',
            field=models.CharField(help_text=b'A short description of the page, used for SEO and not displayed to the user.', max_length=2000, verbose_name='Meta Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='page_meta_keywords',
            field=models.CharField(help_text=b'A short list of keywords of the page, used for SEO and not displayed to the user.', max_length=2000, verbose_name='Meta Page Keywords', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='sharable',
            field=models.BooleanField(default=False, help_text=b'Is URL a sharable URL'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='sitemap_changefreq',
            field=models.CharField(default=b'monthly', help_text=b'How frequently does page content update', max_length=255, verbose_name='Sitemap Change Frequency', choices=[(b'never', 'Never'), (b'yearly', 'Yearly'), (b'monthly', 'Monthly'), (b'weekly', 'Weekly'), (b'daily', 'Daily'), (b'hourly', 'Hourly'), (b'always', 'Always')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='sitemap_priority',
            field=models.CharField(default=b'0.5', max_length=255, blank=True, help_text=b'Sitemap priority', null=True, verbose_name=b'Sitemap Priority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='social_share_image',
            field=models.ForeignKey(related_name='clientset_clientsetcategory_social_images', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='media.Image', help_text=b'Standards for the social share image vary, but an image at least 300x200px should work well.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='social_share_type',
            field=models.CharField(default=b'article', choices=[(b'article', b'Article'), (b'book', b'Book'), (b'profile', b'Profile'), (b'website', b'Website'), (b'video.movie', b'Video - Movie'), (b'video.episode', b'Video - Episode'), (b'video.tv_show', b'Video - TV Show'), (b'video.other', b'Video - Other'), (b'music.song', b'Music - Song'), (b'music.album', b'Music - Album'), (b'music.radio_station', b'Music - Playlist'), (b'music.radio_station', b'Music - Radio Station')], max_length=255, blank=True, null=True, verbose_name=b'Social type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='tiny_url',
            field=models.CharField(help_text=b'Tiny URL used for social sharing', max_length=255, null=True, verbose_name='tiny url', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsetcategory',
            name='twitter_author_id',
            field=models.CharField(help_text=b'Twitter handle, including "@" e.g. @cgpartners', max_length=255, null=True, verbose_name=b'Twitter Admin ID', blank=True),
            preserve_default=True,
        ),
    ]
