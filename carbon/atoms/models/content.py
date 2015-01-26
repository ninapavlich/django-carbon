from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from .abstract import *


class PublishableAtom(models.Model):

    help = {
        'publication_status': "Current publication status",
        'publish_on_date': "Object state will be set to 'Published' on this date.",
        'expire_on_date': "Object state will be set to 'Expired' on this date.",
    }

    DRAFT = 10
    REVIEW = 20
    PUBLISHED = 100
    EXPIRED = 30
    UNPUBLISHED = 40
    PUB_STATUS_CHOICES = (
        (DRAFT, _("Draft")),
        (REVIEW, _("Needs Review")),
        (PUBLISHED, _("Published")),
        (EXPIRED, _("Expired")),
        (UNPUBLISHED, _("Unpublished")),
    )

    publication_date = models.DateTimeField(_('Publication Date'), blank=True, null=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_published_by', 
        on_delete=models.SET_NULL)

    publication_status = models.IntegerField(choices=PUB_STATUS_CHOICES, 
        default=DRAFT, help_text=help['publication_status'])
    

    publish_on_date = models.DateTimeField(_('Publish on Date'), 
        blank=True, null=True, help_text=help['publish_on_date'])
    expire_on_date = models.DateTimeField(_('Expire on Date'), 
        blank=True, null=True, help_text=help['expire_on_date'])

    def is_published(self):

        if self.publication_status == PublishableAtom.PUBLISHED:

            if self.publish_on_date and now() < self.publish_on_date:
                return False

            if self.expire_on_date and now() > self.expire_on_date:
                return False

            return True

        return False

    def save(self, *args, **kwargs):

        has_been_published = False
        if self.pk is not None and self.publication_status == PublishableAtom.PUBLISHED:
            original = type(self).objects.get(pk=self.pk)
            if original.publication_status != self.publication_status:
                has_been_published = True

        #If just published, set published date
        if has_been_published and not self.publication_date:
            self.publication_date = now()

        super(PublishableAtom, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SEOAtom(models.Model):
   
    help = {
        'page_meta_description': "A short description of the page, used for SEO and not displayed to the user.",
        'page_meta_keywords': "A short list of keywords of the page, used for SEO and not displayed to the user.",
        'is_searchable': "Allow search engines to index this object and display in sitemap.",
        'in_sitemap':"Is in sitemap",
        'noindex':"Robots noindex",
        'nofollow':"Robots nofollow",
        'sitemap_changefreq': "How frequently does page content update",
        'sitemap_priority': "Sitemap priority",
    }

    NEVER = 'never'
    YEARLY = 'yearly'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    DAILY = 'daily'
    HOURLY = 'hourly'
    ALWAYS = 'always'
    CHANGE_FREQ_CHOICES = (
        (NEVER, _("Never")),
        (YEARLY, _("Yearly")),
        (MONTHLY, _("Monthly")),
        (WEEKLY, _("Weekly")),
        (DAILY, _("Daily")),
        (HOURLY, _("Hourly")),
        (ALWAYS, _("Always")),
    )

    #SEO
    page_meta_description = models.CharField(_('Meta Description'), 
        max_length=2000, blank=True, help_text=help['page_meta_description'])
    page_meta_keywords = models.CharField(_('Meta Page Keywords'), 
        max_length=2000, blank=True, help_text=help['page_meta_keywords'])

    is_searchable = models.BooleanField(default=True, help_text=help['is_searchable'])
    in_sitemap = models.BooleanField(default=True, help_text=help['in_sitemap'])
    noindex = models.BooleanField(default=False, help_text=help['noindex'])
    nofollow = models.BooleanField(default=False, help_text=help['nofollow'])
    sitemap_changefreq = models.CharField(_('Sitemap Change Frequency'), max_length=255, 
        default=MONTHLY, choices=CHANGE_FREQ_CHOICES,help_text=help['sitemap_changefreq'])
    sitemap_priority = models.CharField("Sitemap Priority", max_length=255, 
        null=True, blank=True, default='0.5', help_text=help['sitemap_priority'])

    class Meta:
        abstract = True

    #Sitemap Properties
    def lastmod(self):
        if hasattr(self, 'modified'):
            return getattr(self, 'modified')
        return None

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except:
            return None

    def changefreq(self, obj):
        return self.changefreq

class SocialSharingAtom(models.Model):  

    help = {
        'sharable': "Is URL a sharable URL",
        'tiny_url': "Tiny URL used for social sharing",
        'social_share_image': "Standards for the social share image vary, but an image at least 300x200px should work well.",
        'facebook_author_id': "Numeric Facebook ID",
        'twitter_author_id': "Twitter handle, including \"@\" e.g. @cgpartners",
        'google_author_id': "Google author id, e.g. the AUTHOR_ID in https://plus.google.com/AUTHOR_ID/posts",
    }

    # -- Choice Data
    MUSIC_SONG = 'music.song'
    MUSIC_ALBUM = 'music.album'
    MUSIC_PLAYLIST = 'music.playlist'
    MUSIC_PLAYLIST = 'music.radio_station'
    VIDEO_MOVIE = 'video.movie'
    VIDEO_EPISODE = 'video.episode'
    VIDEO_TV_SHOW = 'video.tv_show'
    VIDEO_OTHER = 'video.other'
    ARTICLE = 'article'
    BOOK = 'book'
    PROFILE = 'profile'
    WEBSITE = 'website' 

    TYPE_CHOICES = (
        (ARTICLE, "Article"),
        (BOOK, "Book"),
        (PROFILE, "Profile"),
        (WEBSITE, "Website"),
        (VIDEO_MOVIE, "Video - Movie"),
        (VIDEO_EPISODE, "Video - Episode"),
        (VIDEO_TV_SHOW, "Video - TV Show"),
        (VIDEO_OTHER, "Video - Other"),
        (MUSIC_SONG, "Music - Song"),
        (MUSIC_ALBUM, "Music - Album"),
        (MUSIC_PLAYLIST, "Music - Playlist"),
        (MUSIC_PLAYLIST, "Music - Radio Station"),
    )

    #SOCIAL
    sharable = models.BooleanField(default=False, 
        help_text=help['sharable'])
    tiny_url = models.CharField(_('tiny url'), max_length=255, 
        help_text=help['tiny_url'], null=True, blank=True)

    social_share_type = models.CharField("Social type", max_length=255, 
        null=True, blank=True, choices=TYPE_CHOICES, default=ARTICLE )
    
    social_share_image = models.ForeignKey(settings.IMAGE_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_social_images',
        help_text=help['social_share_image'], on_delete=models.SET_NULL)

    facebook_author_id = models.CharField("Facebook Author ID", max_length=255, 
        null=True, blank=True, help_text=help['facebook_author_id'])
    twitter_author_id = models.CharField("Twitter Admin ID", max_length=255, 
        null=True, blank=True, help_text=help['twitter_author_id'])
    google_author_id = models.CharField("Google Admin ID", max_length=255, 
        null=True, blank=True, help_text=help['google_author_id'])

    

    class Meta:
        abstract = True

    def get_sharing_url(self, service):
        try:
            return self.get_absolute_url()     
        except:
            return None


class ContentAtom(models.Model):
    help = {
        'content': "",
        'image':"",
        'authors': "",
        'editors': "",
        'allow_comments':""

    }

    content = models.TextField(_('content'), help_text=help['content'], null=True, blank=True)

    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_authors', help_text=help['authors'])

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_editors', help_text=help['editors'])
   
    allow_comments = models.BooleanField(default=False, 
        help_text=help['allow_comments'])

    class Meta:
        abstract = True

class HasImageAtom(models.Model):
    help = {
        'image': "Featured image",
    }
    image = models.ForeignKey(settings.IMAGE_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_images',
        help_text=help['image'], on_delete=models.SET_NULL)

    def image_preview(self):
        if self.image:
            try:
                return "<img src='%s' alt='%s' />"%(self.image.thumbnail.url, self.image.alt)
            except:
                return "Error displaying image"
        else:
            return "-- No image --"

    class Meta:
        abstract = True        

class ModerationAtom(models.Model):

    help = {
        'moderation_status': "",
        'user':"",
        'content_cleaned':"Cleaned content",
        'moderation_comment':"Comment from moderator"
    }

    DRAFT = 10
    REVIEW = 20
    PUBLISHED = 100
    REJECTED = 50
    MODERATION_STATUS_CHOICES = (
        (DRAFT, _("Draft")),
        (REVIEW, _("Needs Review")),
        (PUBLISHED, _("Published")),
        (REJECTED, _("Rejected")),
    )

    moderation_status = models.IntegerField(choices=MODERATION_STATUS_CHOICES, 
        default=DRAFT, help_text=help['moderation_status'])

    moderation_comment = models.TextField(_('Moderation Comment'), blank=True,
        help_text=help['moderation_comment'])

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_user',
        help_text=help['user'])
    
    cleaned_content = models.TextField(_('Cleaned Content'), blank=True,
        help_text=help['content_cleaned'])


    def is_published(self):

        if self.moderation_status == ModerationAtom.PUBLISHED:

            return True
            
        return False

    class Meta:
        abstract = True


class TagMolecule(VersionableAtom, AddressibleAtom, PublishableAtom, SEOAtom, SocialSharingAtom,):

    class Meta:
        abstract = True      

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

class CategoryMolecule(VersionableAtom, HierarchicalAtom, AddressibleAtom, PublishableAtom, SEOAtom, SocialSharingAtom,):
    #Basically just a tag but with hierarchy
    item_class = None

    class Meta:
        abstract = True

    def get_items(self):
        if not self.item_class:
            raise NotImplementedError('Class should specify an item_class value')
            self.item_class.objects.filter(category=self).order_by('order')

    def get_item_objects(self):
        items = self.get_items()
        return [item.item for item in items]

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")


class OrderedItemMolecule(VersionableAtom,):

    help = {
        'order': "",
    }

    #When implementing, specify item and tag FKs:
    #tag = models.ForeignKey('app.Model')
    #item = models.ForeignKey('app.Model')
    order = models.IntegerField(default=0, help_text=help['order'])

    class Meta:
        abstract = True  


class ContentMolecule(VersionableAtom, AddressibleAtom, PublishableAtom, SEOAtom, SocialSharingAtom, ContentAtom, HasImageAtom):
    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

class UserInputMolecule(VersionableAtom, AddressibleAtom, PublishableAtom, ContentAtom, ModerationAtom):
    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")