import os 
import urllib2

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.template import Template as DjangoTemplate
from django.template import loader
from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.utils.module_loading import import_by_path
from django.utils.text import slugify
from django.utils.text import Truncator
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from slimit import minify
from csscompressor import compress


from carbon.utils.slugify import unique_slugify
from carbon.utils.template import get_page_templates, get_page_templates_raw

from carbon.atoms.models.abstract import *

def title_file_name( instance, filename ):
    
    subfolder = (instance.__class__.__name__).lower()

    file, extension = os.path.splitext( filename )    
    #if instance.clean_filename_on_upload:
    #filename     = "%s%s"%(slugify(filename[:245]), extension)
    filename     = filename.lower()

    full_path = '/'.join( [ subfolder, filename ] )

    #if instance.allow_overwrite==True:
    if instance.file_source.storage.exists(full_path):
        instance.file_source.storage.delete(full_path)

    #if instance.allow_overwrite==True:
    if instance.file_minified.storage.exists(full_path):
        instance.file_minified.storage.delete(full_path)
        
    return full_path

def source_file_name( instance, filename ):
    
    subfolder = (instance.__class__.__name__).lower()

    file, extension = os.path.splitext( filename )    
    #if instance.clean_filename_on_upload:
    filename     = "%s%s"%(slugify(filename[:245]), extension)
    filename     = filename.lower()

    full_path = '/'.join( [ subfolder, filename ] )

    #if instance.allow_overwrite==True:
    if instance.file_source.storage.exists(full_path):
        instance.file_source.storage.delete(full_path)
        
    return full_path

def minified_file_name( instance, filename ):
    print 'mininifed file name: %s'%(filename)
    
    subfolder = (instance.__class__.__name__).lower()

    print 'subfolder? %s'%(subfolder)

    file, extension = os.path.splitext( filename )   
    print 'file %s extension %s'%(file, extension) 
    #if instance.clean_filename_on_upload:
    filename     = "%s%s%s"%(slugify(filename[:245]), '.min', extension)
    filename     = filename.lower()

    print 'finally? %s'%(filename)

    full_path = '/'.join( [ subfolder, filename ] )

    #if instance.allow_overwrite==True:
    if instance.file_minified.storage.exists(full_path):
        instance.file_minified.storage.delete(full_path)
        
    return full_path

def get_storage():
    storage = import_by_path(settings.MEDIA_STORAGE)()
    return storage

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

    def render(self, context):

        file_templates = get_page_templates_raw()

        
        #Add DB Templates
        all_templates = self.__class__.objects.all()
        for template in all_templates:
            key = 'template_%s'%(template.slug)
            context[key] = DjangoTemplate(template.get_content())

        if self.custom_template:
            return DjangoTemplate(self.custom_template).render(context)
        else:
            template = loader.get_template(self.file_template)
            return template.render(context)

    def generate_slug(self):
        unique_slugify(self, self.title, 'slug', None, '_')
        return self.slug


    def save(self, *args, **kwargs):

        if self.slug:
            self.slug = self.slug.replace("-", "_")

        #Clear html template if custom content is defined
        if self.custom_template != None and self.custom_template != '':
            self.file_template = None

        super(TemplateMolecule, self).save(*args, **kwargs)


    class Meta:
        ordering = ['title']
        abstract = True

  
class BaseFrontendPackage(VersionableAtom, TitleAtom):

    help = {
        'title':"File Name",
        'slug':"The filename for this item, without '.min' or the file extension",
        'source':"Copy the un-minified source",
        'minified':"Copy the minified source"
    }

    
    source = models.BooleanField(default=True, help_text=help['source'])
    minified = models.BooleanField(default=True, help_text=help['minified'])
    
    file_source = models.FileField(upload_to=title_file_name, blank=True, null=True, storage=get_storage())
    file_minified = models.FileField(upload_to=title_file_name, blank=True, null=True, storage=get_storage())

    def get_children(self):
        #Override in subclass
        return []

    def get_extension(self):
        #Override in subclass
        return '.txt'

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains",)


    def render(self, save=True):
        source = '/* %s - v%s */%s'%(self.title, self.version, self.get_source())
        minified_source = '/* %s - v%s */%s'%(self.title, self.version, self.minify(source))
        source_file = ContentFile(source)
        minified_file = ContentFile(minified_source)
        
        source_name = "%s%s"%(self.slug, self.get_extension())
        minified_name = "%s.min%s"%(self.slug, self.get_extension())

        self.file_source.save(source_name, source_file, save=save)
        self.file_minified.save(minified_name, minified_file, save=save)


    def minify(self, source):
        #Override in subclass
        return source

    def get_source(self):
        #return concatenated source files
        source = ''
        for child in self.get_children():
            source += child.render()

        return source

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

    def minify(self, source):
        #Override in subclass
        return compress(source)

    # def get_children(self):
    #     return CSSResource.objects.filter(parent=self).order_by('order')



class JSPackage(BaseFrontendPackage):
    class Meta:
        abstract = True

    def get_extension(self):
        return '.js'

    def minify(self, source):
        #Override in subclass
        return minify(source, mangle=True, mangle_toplevel=True)

    # def get_children(self):
    #     return JSResource.objects.filter(parent=self).order_by('order')
    

class BaseFrontendResource(VersionableAtom, TitleAtom, OrderedItemAtom):

    help = {
        'custom_source': "Set the source of this resource",
        'file_source_url':"Choose an existing external resource; choose its URL",
        'title':"",
        'slug':"The filename for this item, without '.min' or the file extension"
    }

    custom_source = models.TextField(_('custom source'), 
        help_text=help['custom_source'], null=True, blank=True)
    file_source_url = models.CharField(_('File Source'), max_length=255, 
        null=True, blank=True,
        help_text=help['file_source_url'])  

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
        compiled = self.compile(source)
        return compiled
    

    def compile(self, source):
        #OVERRIDE IN SUBCLASS
        return source
        

    def get_source(self):
        if self.custom_source:
            return self.custom_source
        elif self.file_source_url:
            response = urllib2.urlopen(self.file_source_url)
            return response.read()
        return ''


    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains",)

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

    def compile(self, source):
        if self.compiler == CSSResource.COMPILER_CSS:
            return source
        #TODO -- add other compilation versions

        return source


    class Meta:
        abstract = True

class JSResource(BaseFrontendResource):
    COMPILER_JS = 'JS'
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

    def compile(self, source):
        if self.compiler == JSResource.COMPILER_JS:
            return source
        #TODO -- add other compilation versions

        return source

    class Meta:
        abstract = True

