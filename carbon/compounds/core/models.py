# -*- coding: utf-8 -*-
import os
import errno
import re
import urllib2, urllib
import tempfile
import traceback
import sys
import shutil
import zipfile
import codecs
import csv
import httplib2
from bs4 import BeautifulSoup

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from gzip import GzipFile

from boto.s3.key import Key
import boto.s3

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.template import Template as DjangoTemplate
from django.template import loader
from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.utils.module_loading import import_string
from django.utils.text import slugify
from django.utils.text import Truncator
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#CSS/JS libs
from slimit import minify
from csscompressor import compress
import sass
# import scss

from carbon.utils.slugify import unique_slugify
from carbon.utils.template import get_page_templates, get_page_templates_raw, get_all_templates

from carbon.atoms.models.abstract import *
from carbon.atoms.models.content import *



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
            limit_choices_to={"model__in": settings.LEGACY_URL_CHOICES}, 
            null=True, blank=True)
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
    def import_links(cls, file, request=None):

        try:
            ignore_files = settings.LEGACY_URL_IGNORE_LIST
            legacy_domain = settings.LEGACY_URL_ARCHIVE_DOMAIN
            legacy_domain_ssl = settings.LEGACY_URL_ARCHIVE_DOMAIN.replace("http://", "https://")
        except:
            ignore_files = []
            legacy_domain = None
            legacy_domain_ssl = None
        
        # print legacy_domain

        if legacy_domain or legacy_domain_ssl:
             # try:
                

            
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
                            try:
                                page_title = soup.title.string.strip()
                            except:
                                page_title == "Untitled %s"%(url)
                                
                            # print "%s (%s)"%(url, page_title)
                            legacy_link = cls.create_legacy_url(url, page_title)
                            

                ctr += 1

            return '%s links parsed' % (items_found)
            # except Exception, e:
            #     return "There was an error reading the .csv file: %s"%(e)
        else:
            return "LEGACY_URL_ARCHIVE_DOMAIN not specified in settings"

    @classmethod
    def create_legacy_url(cls, target_url, target_name, referer_url=None, referer_title=None):
        
        path = cls.clean_path(target_url)
        
        if path:
            link, link_created = cls.objects.get_or_create(url=path)

            if link_created or path != target_name:
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

########################################################################
## MENU GROUPS #########################################################
########################################################################


class MenuItem(VersionableAtom, HierarchicalAtom, LinkAtom, PublishableAtom):
    
    publish_by_default = True

    help = {
    }

    
    #Point to an object
    try:
        content_type = models.ForeignKey(ContentType, 
            limit_choices_to={"model__in": settings.MENU_MODEL_CHOICES}, 
            null=True, blank=True)
    except:
        content_type = models.ForeignKey(ContentType, null=True, blank=True)

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def generate_path(self):
        if self.content_object:
            if hasattr(self.content_object, 'get_absolute_url'):
                return self.content_object.get_absolute_url()
        
        return self.path_override


    def get_link(self):
        '<a href="%s" target="%s" class="%s" %s>%s</a>'%(self.get_path, self.target, self.css_classes, self.title, self.extra_attributes)


    def save(self, *args, **kwargs):

        #Use title if not specified
        if not self.title and self.content_object:
            try:
                self.title = self.content_object.title
            except:
                pass

        super(MenuItem, self).save(*args, **kwargs)

    
    class Meta:
        abstract = True
        ordering = ['order']
    


class AdminAppGroup( VersionableAtom, AddressibleAtom ):
    class Meta:
        abstract = True

    def get_children(self):
        if not self.item_class:
            raise NotImplementedError('Class should specify an item_class value')
        return self.item_class.objects.filter(parent=self).order_by('order')

class AdminAppLink(VersionableAtom, AddressibleAtom):

    parent = models.ForeignKey('AdminAppGroup', blank = True, null = True)

    help = {
        'model_path': "e.x. blog.models.BlogArticle",
    }

    model_path = models.CharField(_("Model Path"), max_length = 255, blank = False,
        db_index=True, help_text=help['model_path'])    



    class Meta:
        abstract = True

class AdminSidebar( VersionableAtom, AddressibleAtom ):
    class Meta:
        abstract = True

    def get_children(self):
        if not self.item_class:
            raise NotImplementedError('Class should specify an item_class value')
        return self.item_class.objects.filter(parent=self).order_by('order')

class AdminLink(VersionableAtom, AddressibleAtom):

    parent = models.ForeignKey('AdminSidebar', blank = True, null = True)

    help = {
        'url': "",
    }

    url = models.CharField(_("URL"), max_length = 255, blank = False,
        db_index=True, help_text=help['url'])      

    class Meta:
        abstract = True    



########################################################################
## TEMPLATES AND RESOURCES #############################################
########################################################################

class Template(VersionableAtom, TitleAtom):

    help = {
        'custom_template': "Override html template file with a custom template.",
        'template':"Choose an existing html template file. This will be overwritten in custom template is filled in.",
        'slug':"This slug can be referenced within templates: {% extends template-slug %}"
    }


    custom_template = models.TextField(_('custom template'), 
        help_text=help['custom_template'], null=True, blank=True)
    file_template = models.CharField(_('Template'), max_length=255, 
        choices=get_page_templates(), null=True, blank=True,
        help_text=help['template'])


    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

    def get_content(self):
        if self.custom_template:
            return self.custom_template
        elif self.file_template:
            loader = FileSystemLoader(self.file_template)
            source = loader.load_template_source(self.file_template)
            return source[0]
        return ''
        
    def generate_slug(self):
        unique_slugify(self, self.title, 'slug', None)
        return self.slug


    def save(self, *args, **kwargs):

        #Clear html template if custom content is defined
        if self.custom_template != None and self.custom_template != '':
            self.file_template = None

        super(Template, self).save(*args, **kwargs)


    class Meta:
        ordering = ['title']
        abstract = True



def title_file_name( instance, filename ):
    
    subfolder = (instance.__class__.__name__).lower()

    file, extension = os.path.splitext( filename )    
    #if instance.clean_filename_on_upload:
    #filename     = "%s%s"%(slugify(filename[:245]), extension)
    filename     = filename.lower()

    full_path = '/'.join( [ subfolder, filename ] )

    #if instance.allow_overwrite==True:
    if hasattr(instance, 'file_source') and instance.file_source.storage.exists(full_path):
        instance.file_source.storage.delete(full_path)

    #if instance.allow_overwrite==True:
    if hasattr(instance, 'file_minified') and instance.file_minified.storage.exists(full_path):
        instance.file_minified.storage.delete(full_path)
        
    return full_path


def get_storage():
    storage = import_string(settings.MEDIA_STORAGE)()
    return storage

class BaseFrontendPackage(VersionableAtom, TitleAtom):

    help = {
        'peg_revision':"While making unstable changes, you may peg the package \
        to last working version number. Then newer packages will only be \
        returned if settings.DEBUG=True. Leave blank to use the lastest version.",
        'title':"File Name",
        'slug':"The filename for this item, without '.min' or the file extension",
        'source':"Copy the un-minified source",
        'minified':"Copy the minified source"
    }

    peg_revision = models.PositiveIntegerField(null=True, blank=True, help_text=help['peg_revision'])
    
    file_source_content = models.TextField(null=True, blank=True)
    error_source_content = models.TextField(null=True, blank=True)

    file_source = models.FileField(upload_to=title_file_name, blank=True, null=True, storage=get_storage())
    file_minified = models.FileField(upload_to=title_file_name, blank=True, null=True, storage=get_storage())

    def get_children(self):
        if not self.item_class:
            raise NotImplementedError('Class should specify an item_class value')
        return self.item_class.objects.filter(parent=self).order_by('order')

    def get_extension(self):
        #Override in subclass
        return '.txt'

    def get_header_type(self):
        #Override in subclass
        return 'text/html'

    def get_src_directories(self):
        output = []
        children = self.get_children()
        for child in children:
            if child.is_source_package():
                output.append(child.get_package_source_folder())

        return output
           

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains",)


    def render(self, save=True):
        source, success, error = self.get_source()

        if success:
            self.error_source_content = None

            try:
                minified_source = self.minify(source)
            except Exception, err:
                self.error_source_content = 'Error minifying %s: %s - %s'%(self.title, traceback.format_exc(), sys.exc_info()[0])
                minified_source = self.file_source_content

            is_different = self.file_source_content != minified_source

            if is_different:
                
                self.file_source_content = minified_source
                
                #Only increment version number on success, and if different
                self.version = self.version+1

                source = u'/* %s - v%s */%s'%(self.title, self.version, source)
                minified_source = u'/* %s - v%s */%s'%(self.title, self.version, minified_source)
                source_file = ContentFile(source)
                minified_file = ContentFile(minified_source)
                
                source_name = self.get_file_name()
                minified_name = self.get_file_name(True)

                self.file_source.save(source_name, source_file, save=save)
                self.file_minified.save(minified_name, minified_file, save=save)

                subfolder = self.__class__.__name__.lower()
                archived_source_path = '/%s/%s/archive/%s/%s'%(subfolder, self.slug, self.version, source_name)
                archived_minifed_path = '/%s/%s/archive/%s/%s'%(subfolder, self.slug, self.version, minified_name)
                self.archive_file(archived_source_path, source)
                self.archive_file(archived_minifed_path, minified_source)

            # else:
            #     print 'success but not different'
        else:
            # print 'error, dont save'
            self.error_source_content = error

    def get_file_name(self, minified=False):
        if minified:
            return u"%s.min%s"%(self.slug, self.get_extension())
        else:
            return u"%s%s"%(self.slug, self.get_extension())

    def get_archived_file_url(self, version, minified=False):

        subfolder = self.__class__.__name__.lower()
        source_name = self.get_file_name(minified)
        source_path = '/%s/%s/archive/%s/%s'%(subfolder, self.slug, version, source_name)
        url = "http://%s.s3.amazonaws.com%s" % (settings.AWS_STORAGE_BUCKET_NAME, source_path)
        return url

    def get_url(self, minified):
        if not self.peg_revision and not settings.DEBUG:
            if minified:
                return '%s?v=%s'%(self.file_minified.url, self.version)
            else:
                return '%s?v=%s'%(self.file_source.url, self.version)
        else:
            return self.get_archived_file_url(self.peg_revision, minified)

    def archive_file(self, source_name, source_file_contents):
        
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME_MEDIA)
        
        headers={'Content-Type': self.get_header_type(), 'Cache-Control': 'max-age=%s'%(settings.CACHE_DURATION)}
        
        is_gzipped = getattr(settings, 'AWS_IS_GZIPPED', False)
        if is_gzipped:
            source_file_contents = self.compress_string(source_file_contents)
            headers['Content-Encoding'] = 'gzip'

        k = Key(bucket)
        k.key = source_name
        k.set_contents_from_string(source_file_contents, headers=headers)
        k.set_acl('public-read')

    def compress_string(self, s):
        """Gzip a given string."""
        zbuf = StringIO()
        zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
        zfile.write(s)
        zfile.close()
        return zbuf.getvalue()




    def increment_version_number(self):
        #Ignore default increment
        pass

    def minify(self, source):
        #Override in subclass
        return source

    def get_source(self):
        #return concatenated source files
        source = ''
        all_success = True
        all_errors = ''
        for child in self.get_children():
            rendered, success, error = child.render()
            if not success:
                all_success = False
                all_errors += "Error in item %s:\n%s\n\n"%(child, error)
                
            
            #Convert rendered content to unicode UTF-8
            try:
                rendered_unicode = unicode(rendered, "utf-8")                
            except:
                #conversion wont work if its already unicode
                rendered_unicode = rendered
            
            slug_decoded = child.slug.decode("utf-8")
            rendered_decoded = rendered_unicode
            source += u'/* --- %s ---- */%s'%(slug_decoded, rendered_decoded)


        # unicode_src = source.decode('ascii')
        # utf8_src = unicode_src.encode('utf-8')

        return (source, all_success, all_errors)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):


        self.render(False)

        super(BaseFrontendPackage, self).save(*args, **kwargs)

        


class CSSPackage(BaseFrontendPackage):
    class Meta:
        abstract = True

    def get_extension(self):
        return '.css'

    def get_header_type(self):
        return 'text/css'

    def minify(self, source):
        #Override in subclass
        return compress(source)

    def get_source(self):
        #prepare all css children
        all_css = self.item_class.objects.all()
        for child in self.get_children():
            child.store_raw_file()

        return super(CSSPackage, self).get_source()

    # def get_children(self):
    #     return CSSResource.objects.filter(parent=self).order_by('order')



class JSPackage(BaseFrontendPackage):
    class Meta:
        abstract = True

    def get_extension(self):
        return '.js'

    def get_header_type(self):
        return 'application/javascript'

    def minify(self, source):
        #Override in subclass
        return minify(source, mangle=True, mangle_toplevel=True)

    # def get_children(self):
    #     return JSResource.objects.filter(parent=self).order_by('order')
    

class BaseFrontendResource(VersionableAtom, TitleAtom, OrderedItemAtom):

    help = {
        'custom_source': "Set the source of this resource",
        'file_source_url':"URL to an existing resource",
        'file_source_path':"Relative source path, if file_source_url is a package",
        'title':"",
        'slug':"The filename for this item, without '.min' or the file extension"
    }

    custom_source = models.TextField(_('custom source'), 
        help_text=help['custom_source'], null=True, blank=True)
    file_source_url = models.CharField(_('File Source'), max_length=255, 
        null=True, blank=True,
        help_text=help['file_source_url'])  
    file_source_path = models.CharField(_('File Source Path'), max_length=255, 
        null=True, blank=True, help_text=help['file_source_path']) 

    def edit_parent(self):
        style="style='width:278px;display:block;'"
        if self.parent:            
            try:
                object_type = type(self.parent).__name__
                url = reverse('admin:%s_%s_change' %(self.parent._meta.app_label,  self.parent._meta.model_name),  args=[self.parent.id] )
                return '<a href="%s" %s>&lt; Edit Parent</a>'%(url, style)
            except:
                return '<span %s>&nbsp;</span>'%(style)
        return '<span %s>&nbsp;</span>'%(style)

    def render(self):
        source = self.get_source()
        compiled, success, error = self.compile(source)
        return (compiled, success, error)
    

    def compile(self, source):
        #OVERRIDE IN SUBCLASS
        success = True
        error = None
        return (source, success, error)
        

    def get_source(self):
        if self.custom_source:
            return self.custom_source
        elif self.file_source_url:
            
            if self.is_source_package():
                get_package_contents(self.file_source_url, self.get_package_folder())

                copy_directory(self.get_package_original_source_folder(), self.get_package_source_folder())

            else:
                response = urllib2.urlopen(self.file_source_url)
                return response.read()

        return ''

    def store_raw_file(self):
        
        raw_source = self.get_source()
        raw_source_name = "%s.%s"%(self.slug, self.get_extension())
        if not self.is_source_package():
            # print 'store_raw_file: %s'%(self.slug)
            write_to_file(raw_source_name, self.get_temp_folder(), raw_source)        

    def get_extension(self):
        #Override in subclass
        return '.txt'

    def is_partial(self):
        return self.slug.startswith('_')

    def is_source_package(self):
        if self.file_source_url:
            is_zip = '.zip' in self.file_source_url
            is_gzip = 'tag.gz' in self.file_source_url
            if is_zip or is_gzip:
                return True
        return False

    def get_temp_folder(self):
        subfolder = '%s_%s'%((self.__class__.__name__).lower(), slugify(settings.SITE_TITLE.lower()))
        directory = "/tmp/%s"%(subfolder)   
        return directory 

    def get_package_folder(self):
        directory = "%s/downloaded/%s"%(self.get_temp_folder(), self.slug)   
        return directory

    def get_package_original_source_folder(self):
        directory = "%s/%s"%(self.get_package_folder(), self.file_source_path)   
        return directory

    def get_package_source_folder(self):
        directory = "%s/%s"%(self.get_temp_folder(), self.slug)   
        return directory

    def get_src_directories(self):
        dirs = [self.get_temp_folder()]
        if self.parent:
            return  dirs + self.parent.get_src_directories()
        else:
            return dirs
    

    def save(self, *args, **kwargs):
        
        source_has_changed = False
        if self.pk is not None:
            original = self.__class__.objects.get(pk=self.pk)
        else:
            original = None

        if original:
            if original.get_source() != self.get_source():
                source_has_changed = True

        super(BaseFrontendResource, self).save(*args, **kwargs)


        if source_has_changed and self.parent:
            #Re-save parent
            self.parent.save()

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains",)

    def __unicode__(self):
        return '%s - %s'%(self.title, self.slug)

    class Meta:
        ordering = ['order']
        abstract = True

class CSSResource(BaseFrontendResource):
    COMPILER_CSS = 'css'
    COMPILER_SCSS = 'scss'
    COMPILER_SASS = 'sass'
    COMPILER_LESS = 'less'
    COMPILER_CHOICES = (
        (COMPILER_CSS, "CSS (None)"),
        (COMPILER_SCSS, "SCSS"),
        (COMPILER_SCSS, "SASS"),
        (COMPILER_LESS, "LESS"),
    )
    #TODO:
    # clevercss
    # less_ruby
    # stylus

    compiler = models.CharField("Compiler / Preprocessor", max_length=255, 
        choices=COMPILER_CHOICES, default=COMPILER_CSS )


    parent = models.ForeignKey('core.CSSPackage')

    def get_extension(self):
        return self.compiler

    def compile(self, source):
        success = True
        error = None
        if self.compiler == CSSResource.COMPILER_CSS:
            return (source, success, error)

        if self.compiler == CSSResource.COMPILER_SCSS or \
            self.compiler == CSSResource.COMPILER_SASS:

            if self.is_partial() or self.is_source_package():
                return ('', success, error)
            else:
            
                try:
                    # scss.config.LOAD_PATHS = self.get_src_directories()

                    # _scss_vars = {}
                    # _scss = scss.Scss(
                    #     scss_vars=_scss_vars,
                    #     scss_opts={
                    #         'compress': True,
                    #         'debug_info': True,
                    #     }
                    # )

                    # compiled = _scss.compile(source)

                    compiled = sass.compile(string=source,include_paths=self.get_src_directories())
                    return (compiled, success, error)

                except Exception, err:
                    error = 'Error compiling %s: %s - %s'%(self.title, traceback.format_exc(), sys.exc_info()[0])
                    print error
                    success = False
                    return (error, success, error)
                    

        #TODO -- add other compilation versions

        return (source, success, error)

    # def replaceSCSSImports( self, css ):
    #     #matches = re.search("^@import.*", css)
    #     matches = re.findall("^@import.*?;", css)

    #     # print "BEFORE"
    #     # print css

    #     print 'matching against %s'%(matches)
    #     if matches:
    #         for match in matches:
    #             import_path = match[match.index('@import')+7:match.index(';')].replace('"', '').replace("'", '').strip()
    #             if import_path != self.slug:
    #                 try:
    #                     source = self.__class__.objects.get(slug=import_path).get_source()
    #                 except:
    #                     source = ''                
    #                 css = css.replace(match, source)
                


    #         # re.search(r"^@import (.+)[0-9a-zA-Z_]", s).group()
    #         # 
    #         # 

    #     # print "AFTER"
    #     # print css
    #     return css


    class Meta:
        abstract = True

class JSResource(BaseFrontendResource):
    COMPILER_JS = 'js'
    COMPILER_COFFEE = 'coffee'

    #TODO:
    # rjsmin
    # yui_js
    # closure_js

    COMPILER_CHOICES = (
        (COMPILER_JS, "JS (None)"),
        (COMPILER_COFFEE, "Coffeescript"),
    )
    compiler = models.CharField("Compiler / Preprocessor", max_length=255, 
        choices=COMPILER_CHOICES, default=COMPILER_JS )

    parent = models.ForeignKey('core.JSPackage')

    def get_extension(self):
        return self.compiler

    def compile(self, source):
        success = True
        error = None
        if self.compiler == JSResource.COMPILER_JS:
            return (source, success, error)

        #TODO -- add other compilation versions

        return (source, success, error)

    class Meta:
        abstract = True


def write_to_file(filename, directory, content):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = "%s/%s"%(directory, filename)
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    # encoded = content.encode('utf-8', ignore)
    try:
        f = codecs.open(file_path, 'w+',encoding='utf-8')
        f.write(content)
    except Exception, err:
        error_message = 'Error storing file %s: %s - %s'%(file_path, traceback.format_exc(), sys.exc_info()[0])
        print error_message

def get_package_contents(url, target_dir):
    # print 'get unzipped: %s'%(url)
    if not os.path.exists(target_dir):
        # print 'create package directory: %s'%(target_dir)
        os.makedirs(target_dir)

    temp_file_name = os.path.basename(url)
    name = os.path.join(target_dir, temp_file_name)
    
    
    if not os.path.exists(name):
        # print 'download file to %s'%(name)
        try:
            name, hdrs = urllib.urlretrieve(url, name)
        except IOError, e:
            print "Can't retrieve %r to %r: %s" % (url, target_dir, e)
            return
    else:
        #print 'file exists. its all good.'
        pass

    is_zip = '.zip' in url
    is_gzip = 'tag.gz' in url

    if is_zip:

        try:
            zf = zipfile.ZipFile(name)
        except zipfile.error, e:
            print "Bad zipfile (from %r): %s" % (url, e)
            return
        zf.extractall(target_dir)



    elif is_gzip:
        print "TODO -- add gzip support"

def copy_directory(src, dest):
    # print 'copy from %s to %s'%(src, dest)
    if os.path.exists(dest):
        try:
            shutil.rmtree(dest)
        except shutil.Error as e:
            print('Directory not removed. Error: %s' % e)

    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)        

    