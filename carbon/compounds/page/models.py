from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from bs4 import BeautifulSoup

from carbon.utils.slugify import unique_slugify
from carbon.atoms.models.abstract import VersionableAtom, HierarchicalAtom, AddressibleAtom
from carbon.atoms.models.content import ContentMolecule, TagMolecule, TemplateMolecule, PublishableAtom

class Page(HierarchicalAtom, ContentMolecule):

    # YOU GOTTA IMPLEMENT THIS:
    # tags = models.ManyToManyField('page.PageTag', null=True, blank=True)

    def get_url_path(self):
        path = self.path
        if path.startswith('/'):
            path = path[1:]

        # if path.endswith('/'):
        #     path = path[:1]
            
        return path

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

    # YOU GOTTA IMPLEMENT THIS:
    # def get_absolute_url(self):
    #     return reverse('pages_page', kwargs = {'path': self.get_url_path() })   

    class Meta:
        abstract = True



class PageTag(TagMolecule):  

    class Meta:
        verbose_name_plural = 'Page Tags'

    # YOU GOTTA IMPLEMENT THIS:
    # def get_absolute_url(self):
    #     return reverse('pages_tag', kwargs = {'path': self.get_url_path() })   

    def get_children(self):
        all_children = Page.objects.filter(tags__in=[self])
        return [child for child in all_children if child.is_published()]

    class Meta:
        abstract = True
        


class MenuItem(VersionableAtom, HierarchicalAtom, AddressibleAtom, PublishableAtom):

    help = {
        'title': "",
        'slug': "",
        'path': "Override path for this menu item",
        'target': "",
        'order':"",
        'css_classes':"Extra css classes to add to "
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

    
    #Point to an object
    try:
        content_type = models.ForeignKey(ContentType, 
            limit_choices_to={"model__in": settings.MENU_MODEL_CHOICES}, null=True, blank=True)
    except:
        content_type = models.ForeignKey(ContentType, null=True, blank=True)

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


    target = models.CharField(_('Target'), max_length=255, help_text=help['target'], 
        choices=TARGET_CHOICES, default=SELF)

    css_classes = models.CharField(_('CSS Classes'), max_length=255, help_text=help['target'], 
        choices=TARGET_CHOICES, default=SELF)

    def get_path(self):
        if self.content_object:
            if hasattr(self.content_object, 'get_absolute_url'):
                return self.content_object.get_absolute_url()
        
        return self.path_override

    def get_link(self):
        '<a href="%s" target="%s" class="%s">%s</a>'%(self.get_path, self.target, self.css_classes, self.title)


    def save(self, *args, **kwargs):

        #Published by default
        if not self.pk:
            self.publication_status = PublishableAtom.PUBLISHED

        super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        abstract = True
    


class LegacyURLReferer(VersionableAtom):

    help = {
        'legacy_url': "",
        'referer_title': "",
        'referer_url': "",
    }

   
    #legacy_url = models.ForeignKey('LegacyURL')

    referer_title = models.CharField(_('Referer Title'), max_length=255, 
        help_text=help['referer_title'], blank=True, null=True)

    referer_url = models.CharField(_('Referer URL'), max_length=255, 
        help_text=help['referer_url'], blank=True, null=True)


    class Meta:
        abstract = True

class LegacyURL(VersionableAtom, AddressibleAtom):

    help = {
        'url': "",
    }

    url = models.CharField(_("URL"), max_length = 255, blank = False,
        db_index=True)
   
    #Point to an object
    try:
        content_type = models.ForeignKey(ContentType, 
            limit_choices_to={"model__in": settings.LEGACY_URL_CHOICES}, null=True, blank=True)
    except:
        content_type = models.ForeignKey(ContentType, null=True, blank=True)

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    
    class Meta:
        abstract = True        

    def get_children(self):
        return []

    @property
    def has_redirect_url(self):
        url = self.get_redirect_url()
        if url:
            return True
        return False

    def get_redirect_url(self):
        if self.path:
            return self.path
        return self.compute_get_redirect_url()  

    def generate_path(self):
        if self.path_override:
            return self.path_override
        if self.content_object:
            try:
                url = self.content_object.get_absolute_url()
                return url
            except:
                print "ERROR RETRIEVING ABSOLUTE URL From %s"%(self.content_object)         
        
        return None

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "url__icontains", "title__icontains",)

    @classmethod
    def import_links(file, request=None):

        try:
            ignore_files = settings.LEGACY_URL_IGNORE_LIST
            legacy_domain = settings.LEGACY_URL_ARCHIVE_DOMAIN
            legacy_domain_ssl = settings.LEGACY_URL_ARCHIVE_DOMAIN.replace("http://", "https://")
        except:
            ignore_files = []
            legacy_domain = None
            legacy_domain_ssl = None
        
        if legacy_domain or legacy_domain_ssl:
            try:
                

                
                items_found = 0

                ctr = 0
                for row in csv.reader(file.read().splitlines()):

                    #dont read from first row -- which contains column titles
                    if ctr > 0:

                        status_check    = row[0].lower()
                        url             = row[1]
                        referer         = row[2]
                        
                        if legacy_domain in url or legacy_domain_ssl in url:
                            
                            is_allowed = True
                            for piece in ignore_files:
                                if piece in url:
                                    is_allowed = False

                            if is_allowed:

                                items_found     += 1
                                                        
                                http = httplib2.Http()
                                status, response = http.request(url)
                                soup = BeautifulSoup(response)  
                                page_title = soup.title.string.strip()
                                print "%s (%s)"%(url, page_title)
                                legacy_link = LegacyURL.create_legacy_url(url, page_title)
                                

                    ctr += 1

                return '%s links parsed' % (items_found)
            except Exception, e:
                return "There was an error reading the .csv file: %s"%(e)

    @classmethod
    def create_legacy_url(cls, target_url, target_name, referer_url=None, referer_title=None):
        link, link_created = cls.objects.get_or_create(url=target_url)

        if link_created or target_url != target_name:
            link.title = target_name
            link.save()


        if referer_url:
            referer_link, referer_created = cls.objects.get_or_create(legacy_url=link,referer_url=referer_url)
            if referer_created:
                if settings.DEBUG:
                    print "Create new referer %s %s to %s"%(referer_title, referer_url, target_url)
                referer_link.referer_title = referer_title
                referer_link.save()

        return link

    @classmethod
    def create_legacy_url(cls, url, title=None):

        path = cls.clean_path(url)

        if not title:
            title = path

        if path:
            legacy_link = cls.create_legacy_url(path, title)

            return legacy_link

        return None

    @classmethod
    def add_referer(cls, referer_url, referer_title, target_url):

        path = cls.clean_path(target_url)
        if path:
            legacy_link = cls.create_legacy_url(path, path, referer_url, referer_title)
            return legacy_link
        return None

    @classmethod
    def clean_path(cls, url):

        legacy_domain = settings.LEGACY_URL_ARCHIVE_DOMAIN
        legacy_domain_ssl = settings.LEGACY_URL_ARCHIVE_DOMAIN.replace("http://", "https://")

        path = url
        path = path.replace(legacy_domain, '')
        path = path.replace(legacy_domain_ssl, '')

        if 'http' in path:
            #print "Must be a different domain %s"%(path)
            return None

        if path == '' or path == None or path == '#':
            return None

        #Make sure path includes starting /
        if path.startswith('/') == False:
            path = '/%s'%path

        return path


    