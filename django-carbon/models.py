from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

class Versionable(models.Model):

    version = models.IntegerField(default=0)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(class)s_created_by')

    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(class)s_modified_by')

    def save(self, *args, **kwargs):
        
        self.increment_version_number()

        super(Versionable, self).save(*args, **kwargs)

    def increment_version_number(self):
        self.version = self.version+1

class Categorizable(models.Model):

    help = {
        'parent': "The display title for this page. No more than 5 words, 28 characters with spaces.",
        'tags': "Tags associated with this item",
        'related': "Other items related to this item",        
    }

    parent = models.ForeignKey('self', blank=True, null=True,
        related_name="children", help_text=help['parent'])

    tags = models.ManyToManyField(settings.TAG_MODEL, blank=True, 
        null=True, related_name='%(class)s_tags', help_text=help['tags'])

    related = models.ManyToManyField('self', blank=True, 
        null=True, related_name='%(class)s_related', help_text=help['related'])

    def get_children(self):
        return self.__class__.objects.filter(parent=self)

class Addressible(Versionable):
   
    help = {
        'title': "The display title for this page. No more than 5 words, 28 characters with spaces.",
        'slug': "Auto-generated page text id for this page.",
        'path': "The URL path to this page, defined page text id.",
        'path_override': "Override to the default page url path defined in 'path' using the format: /my/custom/path",
        'temporary_redirect': "Temporarily redirect to a different path",
        'permanent_redirect': "Permanently redirect to a different path",
        'page_meta_description': "A short description of the page, used for SEO and not displayed to the user.",
        'page_meta_keywords': "A short list of keywords of the page, used for SEO and not displayed to the user.",
        'allow_robots': "Allow search engines to index this object.",
        'changefreq': "How frequently does page content update"
    }

    YEARLY = 'yearly'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    DAILY = 'daily'
    CHANGE_FREQ_CHOICES = (
        (YEARLY, _("Yearly")),
        (MONTHLY, _("Monthly")),
        (WEEKLY, _("Weekly")),
        (DAILY, _("Deaily")),
    )

    title = models.CharField(_('Page Title'), max_length=255, 
        help_text=help['title'])

    slug = models.CharField(_('Text ID'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])

    path = models.CharField(_('path'), max_length=255, unique=True,
        help_text=help['path'])
    path_override = models.CharField(_('path override'), max_length=255,
        blank=True, help_text=help['path_override'])

    temporary_redirect = models.CharField(_('Temporary Redirect'), max_length=255,
        blank=True, help_text=help['temporary_redirect'])
    permanent_redirect = models.CharField(_('Permanent Redirect'), max_length=255,
        blank=True, help_text=help['redirect_path'])

    #SEO
    page_meta_description = models.CharField(_('Meta Description'), 
        max_length=2000, blank=True, help_text=help['page_meta_description'])
    page_meta_keywords = models.CharField(_('Meta Page Keywords'), 
        max_length=2000, blank=True, help_text=help['page_meta_keywords'])

    allow_robots = models.BooleanField(default=False, 
        help_text=help['allow_robots'])
    changefreq = models.CharField(_('Meta Page Keywords'), 
        max_length=2000, blank=True, help_text=help['changefreq'])

    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains",)

    def build_path(self):
        if self.path_override:
            return self.path_override
        elif hasattr(self, 'parent') and getattr(self, 'parent')!= None and hasattr(getattr(self, 'parent'), 'path'):
            #if object has a parent and parent has a path:
            parent = getattr(self, 'parent')
            return "%s%s/" % (parent.path, self.slug)
        else:
            return "/%s/" % self.slug

    def get_absolute_url(self):
        return self.path

    #Sitemap Properties
    def lastmod(self):
        return obj.modified

    def location(self, obj):
        return obj.get_absolute_url()

    def changefreq(self, obj):
        return self.changefreq


    def save(self, *args, **kwargs):

        new_path = self.build_path()

        #If path has changed, notify children
        if self.path != new_path:
            self.path = new_path
            [p.save() for p in self.get_children()]

        super(Addressible, self).save(*args, **kwargs)


class Publishable(models.Model):

    help = {
        'publication_status': "The display title for this page. No more than 5 words, 28 characters with spaces.",
        'publish_date': "Object state will be set to 'Published' on this date. (Note: Requires Cron)",
        'expire_date': "Object state will be set to 'Expired' on this date. (Note: Requires Cron)",        
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

    publication_status = models.IntegerField(choices=PUB_STATUS_CHOICES, 
        default=DRAFT, help_text=help['publication_status'])
    publish_date = models.DateTimeField(_('Publish on Date'), auto_now=True, 
        blank=True, null=True, help_text=help['publish_date'])
    expire_date = models.DateTimeField(_('Expire on Date'), auto_now=True, 
        blank=True, null=True, help_text=help['expire_date'])

    def check_dates(self):
        
        #TODO
        if self.publish_date and now() >= self.publish_date:
            self.state = PUBLISHED
            self.save()

        if self.expire_date and now() <= self.expire_date:
            self.state = EXPIRED
            self.save()


class Accessible(models.Model):

    help = {
        'access_restriction': "Restrict access to the item",
        'password':"Password to use if access_restriction is set to Password"
    }

    OPEN = 1
    REGISTERED_USERS = 2
    PASSWORD = 3
    USER_WHITELIST = 4
    USER_BLACKLIST = 5
    CUSTOM = 6
    ACCESS_CHOICES = (
        (OPEN, _("Open")),
        (REGISTERED_USERS, _("Registered Users")),
        (PASSWORD, _("Password")),
        (USER_WHITELIST, _("User Whitelist")),
        (USER_BLACKLIST, _("User Blacklist")),
        (CUSTOM, _("Custom")),
    )

    access_restriction = models.IntegerField(choices=ACCESS_CHOICES, 
        default=OPEN, help_text=help['access_restriction'])

    password = models.CharField(_('Encrypted Password'), max_length=255, 
        null=True, blank=True, help_text=help['password'])

    user_whitelist = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(class)s_user')
    user_blacklist = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(class)s_user')

    def access_allowed(self, request):
        if self.access_restriction == OPEN:
            return True
        elif self.access_restriction == REGISTERED_USERS:
            return (request.user and request.user.is_authenticated())
        elif self.access_restriction == PASSWORD:
            #Check if there is a password stored in the cookies
            #If not, prompt for password

        elif self.access_restriction == PASSWORD.USER_WHITELIST:
            if request.user and request.user.is_authenticated():
                return request.user in self.user_whitelist
            else:
                return False

        elif self.access_restriction == PASSWORD.USER_BLACKLIST:
            if request.user and request.user.is_authenticated():
                return request.user not in self.user_whitelist
            else:
                return False

        elif self.access_restriction == PASSWORD.CUSTOM:
            return self.custom_access_allowed(request)

        return True


    def custom_access_allowed(self, request):
        #OVERRIDE IN SUBCLASS
        return True

class Sociable(models.Model):

    help = {
        'allow_sharing': "Allow item to be shared on social networks"
    }

    allow_sharing = models.BooleanField(default=False, 
        help_text=help['allow_sharing'])

    #TODO -- other social integrations

    def get_sharing_link(self, service):
        #TODO
        return 'TODO: share link'

class Content(models.Model):
    help = {
        'content': "Allow item to be shared on social networks",
        'image':"",
        'authors': "",
        'editors': "",
        'pub_date': "",
        'display_pub_date':""

    }

    content = models.TextField(_('content'), max_length=CONTENT_MAX_LENGTH,
        help_text=help['content'])

    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_authors', help_text=help['authors'])

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_editors', help_text=help['editors'])

    pub_date = models.DateField('Publication Date', blank=True, null=True,
        help_text=help['pub_date'])
    display_pub_date = models.BooleanField( _("Display Publication Date"), 
        default = True, help_text=help['display_pub_date'])

class Related(models.Model)
    
    # Related item
    content_type = models.ForeignKey(ContentType,
             verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", 
        fk_field="object_pk")

class UserInput(Versionable, Related, Content):

    help = {
        'allow_sharing': "Allow item to be shared on social networks",
        'moderation_status': "",
        'content_cleaned':"",
        'admin_comment':""
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(class)s_user',
        help_text=help['user'])
    
    cleaned_content = models.TextField(_('Cleaned Content'), blank=True,
        help_text=help['content_cleaned'])

    admin_comment = models.TextField(_('Cleaned Content'), blank=True,
        help_text=help['admin_comment'])

class Tag(Versionable, Categorizable, Addressible):
    pass