from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

# -- Level 1
class Versionable(models.Model):

    model_settings = {}

    version = models.IntegerField(default=0)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_created_by')

    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_modified_by')

    admin_note = models.TextField(_('admin note'), blank=True, null=True)

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super(Versionable, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        
        self.increment_version_number()

        super(Versionable, self).save(*args, **kwargs)

    def increment_version_number(self):
        self.version = self.version+1

# -- Level 2
class Addressible(models.Model):
   
    help = {
        'title': "The display title for this page. No more than 5 words, 28 characters with spaces.",
        'slug': "Auto-generated page text id for this page.",
        'parent': "Hierarchical parent of this item. Used to define path.",
        'path': "The URL path to this page, defined page text id.",
        'path_override': "Override to the default page url path defined in 'path' using the format: /my/custom/path",
        'temporary_redirect': "Temporarily redirect to a different path",
        'permanent_redirect': "Permanently redirect to a different path",
        'page_meta_description': "A short description of the page, used for SEO and not displayed to the user.",
        'page_meta_keywords': "A short list of keywords of the page, used for SEO and not displayed to the user.",
        'allow_robots': "Allow search engines to index this object.",
        'changefreq': "How frequently does page content update",
        'sharable': "Is URL a sharable URL",
        'tiny_url': "Tiny URL used for social sharing"
    }

    model_settings = {}

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

    parent = models.ForeignKey('self', blank=True, null=True,
        related_name="children", help_text=help['parent'])

    path = models.CharField(_('path'), max_length=255, unique=True,
        help_text=help['path'])
    path_override = models.CharField(_('path override'), max_length=255,
        blank=True, help_text=help['path_override'])

    temporary_redirect = models.CharField(_('Temporary Redirect'), max_length=255,
        blank=True, help_text=help['temporary_redirect'])
    permanent_redirect = models.CharField(_('Permanent Redirect'), max_length=255,
        blank=True, help_text=help['permanent_redirect'])

    #SOCIAL
    sharable = models.BooleanField(default=False, 
        help_text=help['sharable'])
    tiny_url = models.CharField(_('tiny url'), max_length=255, unique=True,
        help_text=help['tiny_url'])

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
        elif self.parent:
            return "%s%s/" % (self.parent.path, self.slug)
        else:
            return "/%s/" % self.slug

    def get_absolute_url(self):
        return self.path

    def get_sharing_url(self, service):
        #TODO
        return self.get_absolute_url()

    #Sitemap Properties
    def lastmod(self):
        if hasattr(self, 'modified'):
            return getattr(self, 'modified')
        return None

    def location(self, obj):
        return obj.get_absolute_url()

    def changefreq(self, obj):
        return self.changefreq

    def get_children(self):
        return self.__class__.objects.filter(parent=self)

    

    def save(self, *args, **kwargs):

        new_path = self.build_path()

        #If path has changed, notify children
        if self.path != new_path:
            self.path = new_path
            [p.save() for p in self.get_children()]

        super(Addressible, self).save(*args, **kwargs)

# -- Level 3       
class Publishable(models.Model):

    help = {
        'publication_status': "The display title for this page. No more than 5 words, 28 characters with spaces."
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
    

    class Meta:
        abstract = True

    

# -- Level 4
class Accessible(models.Model):

    help = {
        'access_restriction': "Restrict access to the item",
        'password':"Password to use if access_restriction is set to Password",
        'publish_date': "Object state will be set to 'Published' on this date. (Note: Requires Cron)",
        'expire_date': "Object state will be set to 'Expired' on this date. (Note: Requires Cron)",
        'require_registered_user' : "Require logged in user"   
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

    require_registered_user = models.BooleanField( _("Required Registered Users"), 
        default = False, help_text=help['require_registered_user'])

    password = models.CharField(_('Encrypted Password'), max_length=255, 
        null=True, blank=True, help_text=help['password'])

    user_whitelist = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_user')

    publish_date = models.DateTimeField(_('Publish on Date'), auto_now=True, 
        blank=True, null=True, help_text=help['publish_date'])
    expire_date = models.DateTimeField(_('Expire on Date'), auto_now=True, 
        blank=True, null=True, help_text=help['expire_date'])

    class Meta:
        abstract = True

    def access_allowed(self, request):
        
        if self.require_registered_user: 
            if not request.user or not request.user.is_authenticated():
                return False


        # elif self.access_restriction == PASSWORD:
        #     #Check if there is a password stored in the cookies
        #     #If not, prompt for password
        #     pass

        user_whitelist = self.user_whitelist.all()
        if len(user_whitelist) > 0:
            if not request.user or not request.user.is_authenticated() \
            or not request.user in user_whitelist:
                return False

        elif self.access_restriction == PASSWORD.CUSTOM:
            custom = self.custom_access_allowed(request)
            if custom == False:
                return False
        
        if self.publish_date and now() < self.publish_date:
            return False

        if self.expire_date and now() > self.expire_date:
            return False

        return True

    def custom_access_allowed(self, request):
        #OVERRIDE IN SUBCLASS
        return True

# # -- Level 5
# class Listable(models.Model):

#     model_name = 'Listable'
    
#     help = {
#         'order': "Simple order of item. May be overwritted in get_order()",
#         'list_title': "Title of item when displayed in lists.",
#         'list_description': "Description of item when displayed in lists",  
#         'list_image': "Image used when item display in lists"      
#     }


#     order = models.IntegerField(default=0, help_text=help['order'])

#     list_title = models.CharField(_('List Title'), max_length=255, 
#         help_text=help['list_title'])

#     list_description = models.TextField(_('List Description'), 
#         help_text=help['list_description'])

#     list_image = models.ForeignKey(get_image_model(model_name), 
#         blank=True, null=True, related_name='%(app_label)s_%(class)s_list_images',
#         help_text=help['list_image'])

#     class Meta:
#         abstract = True

    

#     def get_order(self, context):
#         #OVERRIDE LOGIC
#         return self.order

#     def save(self, *args, **kwargs):
        
#         if not self.list_title and hasattr(self, 'title'):
#             self.list_title = getattr(self, 'title')

#         super(Listable, self).save(*args, **kwargs)

# -- Level 6
class Categorizable(models.Model):

    help = {
        'categories': "Categories associated with this item",
        'tags': "Tags associated with this item",
        'related': "Other items related to this item",        
    }


    categories = models.ManyToManyField(settings.TAG_MODEL, blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_categories', help_text=help['categories'])

    tags = models.ManyToManyField(settings.TAG_MODEL, blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_tags', help_text=help['tags'])

    related = models.ManyToManyField('self', blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_related', help_text=help['related'])

    # Related item
    content_type = models.ForeignKey(ContentType,
             verbose_name=_('content type'),
            related_name="content_type_set_for_%(app_label)s_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", 
        fk_field="object_pk")

    class Meta:
        abstract = True

# -- Level 7
class Content(models.Model):
    help = {
        'content': "Allow item to be shared on social networks",
        'image':"",
        'authors': "",
        'editors': "",
        'pub_date': "",
        'display_pub_date':"",
        'allow_comments':""

    }

    content = models.TextField(_('content'), help_text=help['content'])

    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_authors', help_text=help['authors'])

    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(app_label)s_%(class)s_editors', help_text=help['editors'])

    pub_date = models.DateField('Publication Date', blank=True, null=True,
        help_text=help['pub_date'])
    display_pub_date = models.BooleanField( _("Display Publication Date"), 
        default = True, help_text=help['display_pub_date'])

    allow_comments = models.BooleanField(default=False, 
        help_text=help['allow_comments'])

    class Meta:
        abstract = True

# -- Level 8
class UserInput(models.Model):

    help = {
        'moderation_status': "",
        'user':"",
        'content_cleaned':"",
        'moderation_comment':""
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

    class Meta:
        abstract = True
