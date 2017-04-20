from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template as DjangoTemplate
from django.template import loader
from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.utils.text import Truncator
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from carbon.utils.slugify import unique_slugify
from carbon.utils.template import get_page_templates, get_page_templates_raw

from carbon.atoms.managers.content import PublishableManager

from .abstract import *


class PublishableAtom(models.Model):
    publish_by_default = False

    help = {
        'publication_status': "Current publication status",
        'publish_on_date': "Object state will be set to 'Published' on this date.",
        'expire_on_date': "Object state will be set to 'Expired' on this date.",
    }

    DRAFT = 10
    REVIEW = 20
    PUBLISHED = 100
    #EXPIRED = 30
    UNPUBLISHED = 40
    PUB_STATUS_CHOICES = (
        (DRAFT, _("Draft")),
        (REVIEW, _("Needs Review")),
        (PUBLISHED, _("Published")),
        # (EXPIRED, _("Expired")),
        (UNPUBLISHED, _("Unpublished")),
    )

    objects = PublishableManager()

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

        #Published by default
        if not self.pk and self.publish_by_default:
            self.publication_status = PublishableAtom.PUBLISHED

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
        'page_meta_description': "A short description of the page, used for SEO and not displayed to the user; aim for 150-160 characters.",
        'page_meta_keywords': "A short list of keywords of the page, used for SEO and not displayed to the user; aim for 150-160 characters.",
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
        'shareable': "Show sharing widget",
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
    shareable = models.BooleanField(default=False, 
        help_text=help['shareable'])
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
    auto_synopsis_length = 30
    help = {
        'content': "",
        'synopsis': ""
    }

    content = models.TextField(_('content'), help_text=help['content'], null=True, blank=True)
    synopsis = models.TextField(_('synopsis'), help_text=help['synopsis'], null=True, blank=True)

    def get_synopsis(self):
        if self.synopsis and self.synopsis != '':
            return self.synopsis
        elif self.content and self.content != '':
            return Truncator(self.content).words(self.auto_synopsis_length, html=True)
        return ''            

    class Meta:
        abstract = True

class HasImageAtom(models.Model):
    help = {
        'image': "Featured image",
    }
    image = models.ForeignKey(settings.IMAGE_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_images',
        help_text=help['image'], on_delete=models.SET_NULL)

    @cached_property
    def image_preview_url(self):
        if self.image:
            return self.image.thumbnail.url
        return None

    def image_preview(self):
        if self.image:
            try:
                url = self.image_preview_url
                return mark_safe("<img src='%s' alt='%s' />"%(url, self.image.alt))
            except:
                return "Error displaying image"
        else:
            return "-- No image --"     

    class Meta:
        abstract = True        


class LinkAtom(models.Model):

    help = {
        'target': "",
        'css_classes':"Extra css classes to add to the item",
        'extra_attributes': "Extra attributes to add to the item"
    }

    

    BLANK = '_blank'
    SELF = '_self'
    PARENT = '_parent'
    TOP = '_top'
    TARGET_CHOICES = (
        (BLANK, _(BLANK)),
        (SELF, _(SELF)),
        (PARENT, _(PARENT)),
        (TOP, _(TOP))        
    )

    url = models.CharField(_("URL"), max_length=255, blank = True, 
        null = True)

    target = models.CharField(_('Target'), max_length=255, 
        help_text=help['target'], choices=TARGET_CHOICES, default=SELF)

    css_classes = models.CharField(_('CSS Classes'), max_length=255, 
        help_text=help['css_classes'], null=True, blank=True, default='')

    extra_attributes = models.CharField(_('Extra Attributes'), max_length=255, 
        help_text=help['extra_attributes'], null=True, blank=True, default='')

    def get_target(self):
        return 'target="%s"'%(self.target)


    class Meta:
        abstract = True    

class ModerationAtom(models.Model):

    help = {
        'moderation_status': "",
        'user':"",
        'content_cleaned':"Cleaned content",
        'moderation_comment':"Comment from moderator"
    }

    SUBMITTED = 10
    REJECTED = 50
    PUBLISHED = 100    
    APPROVED = 150
    MODERATION_STATUS_CHOICES = (
        (SUBMITTED, _("Submitted by User")),
        (PUBLISHED, _("Published")),
        (REJECTED, _("Rejected by Moderator")),
        (APPROVED, _("Approved by Moderator")),
    )

    moderation_status = models.IntegerField(choices=MODERATION_STATUS_CHOICES, 
        default=SUBMITTED, help_text=help['moderation_status'])

    moderation_comment = models.TextField(_('Moderation Comment'), blank=True,
        help_text=help['moderation_comment'])

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_user',
        help_text=help['user'])
    
    cleaned_content = models.TextField(_('Cleaned Content'), blank=True,
        help_text=help['content_cleaned'])


    def is_moderated(self):

        if self.moderation_status == ModerationAtom.PUBLISHED:

            return True
            
        return False

    class Meta:
        abstract = True





class ContentMolecule(VersionableAtom, AddressibleAtom, PublishableAtom, SEOAtom, SocialSharingAtom, ContentAtom, HasImageAtom):
    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

class CategoryMolecule(HierarchicalAtom, ContentMolecule):
    #Basically just a tag but with hierarchy
    item_class = None
    item_classes = None
    category_property_name = 'category'

    class Meta:
        abstract = True

    @cached_property
    def category_children(self):
        items = self.get_items()
        output = []
        for child in items:
            if child.is_published():
                if hasattr(self, 'item'):
                    output.append(child.item)
                else:
                    output.append(child)

        return output

    def get_items(self):
        if not self.item_class and not self.item_classes:
            raise NotImplementedError('Class should specify an item_class or item_classes value')
        
        if self.item_classes:
            [item_class.objects.published().filter(**{ self.tag_property_name: self }).order_by('order') for item_class in self.item_classes]
        else:
            return self.item_class.objects.published().filter(**{ self.tag_property_name: self }).order_by('order')

    def get_children(self):
        return self.category_children

    def get_next_item(self, item):
        children = self.get_children()
        next_index = (children.index(item) + 1) % len(children)
        return children[next_index]

    def get_previous_item(self, item):
        children = self.get_children()
        previous_index = (children.index(item) + len(children) - 1) % len(children)
        return children[previous_index]

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")



class TagMolecule(ContentMolecule):
                
    item_class = None
    item_classes = None
    tag_property_name = 'tags'

    class Meta:
        abstract = True    

    @cached_property
    def tag_children(self):  
        if not self.item_class and not self.item_classes:
            raise NotImplementedError('Class should specify an item_class or item_classes value')
        
        if self.item_classes:
            [item_class.objects.published().filter(**{ self.tag_property_name: self }).order_by('order') for item_class in self.item_classes]
        else:
            return self.item_class.objects.published().filter(**{ self.tag_property_name: self }).order_by('order')

    def get_children(self):
        return self.tag_children        

    def get_next_item(self, item):
        children = self.get_children()
        next_index = (children.index(item) + 1) % len(children)
        return children[next_index]

    def get_previous_item(self, item):
        children = self.get_children()
        previous_index = (children.index(item) + len(children) - 1) % len(children)
        return children[previous_index]

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

class UserInputMolecule(VersionableAtom, AddressibleAtom, PublishableAtom, ContentAtom, ModerationAtom):
    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")


class UpvoteDownvoteFlagMolecule(VersionableAtom):
    class Meta:
        abstract = True

    help = {
        'type': "",
        'voter':""
    }

    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    FLAG = 'flag'
    VOTE_CHOICES = (
        (UPVOTE, _(UPVOTE)),
        (DOWNVOTE, _(DOWNVOTE)),
        (FLAG, _(FLAG))  
    )

    type = models.CharField(_('Vote Choices'), max_length=255, 
        help_text=help['type'], choices=VOTE_CHOICES)

    voter = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_user',
        help_text=help['voter'])

    # Implement what user is voting on:
    # item = models.ForeignKey('blog.BlogComment')

class HasSlidesMolecule(models.Model):
    #TODO: Defile
    #slide_class

    @cached_property
    def slides(self):
        return self.slide_class.objects.filter(parent=self).order_by('order').select_related('slide_image')

    class Meta:
        abstract = True

class SlideMolecule(VersionableAtom, OrderedItemAtom):
    
    # parent = models.ForeignKey('app.Model')
    slide_image = models.ForeignKey('media.Image', null=True, blank=True)

    class Meta:
        ordering = ['order']
        abstract = True

        