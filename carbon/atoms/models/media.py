import os
import time

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from .abstract import *
from .content import HasImageAtom


#HELPER FUNCTIONS

def title_file_name( instance, filename ):
    """Generate File Name"""

    subfolder = (instance.__class__.__name__).lower()

    filename, extension = os.path.splitext( filename )    
    if instance.clean_filename_on_upload:
        short_title = slugify(filename[:50])    
        filename        = "%s-%s%s" % ( short_title, str( time.time() )[0:10], extension )
    
        filename        = filename.lower()

    return '/'.join( [ subfolder, filename ] )


def clean_path(path):
    file, extension = os.path.splitext( path )

    split = file.split('/')
    file_name = split[-1]
    file_name = file_name.replace("_", "-")
    words = file_name.split("-")
    
    #Don't include auto-generated number from above, if included in filename
    last_word = words[-1]
    is_auto_number = last_word.isdigit() and len(last_word)==10
    if is_auto_number:
        words = words[0:-1]

    combined = ' '.join(words).title()
    
    return combined



 


def get_storage(type):
    if type=='BaseImage':
        storage = import_by_path(settings.IMAGE_STORAGE)()
    elif type=='BaseMedia':
        storage = import_by_path(settings.MEDIA_STORAGE)()
    elif type=='BaseSecureImage':
        storage = import_by_path(settings.SECURE_IMAGE_STORAGE)()
    elif type=='BaseSecureMedia':
        storage = import_by_path(settings.SECURE_MEDIA_STORAGE)()
    return storage



class RichContentAtom(models.Model):
    """
    This class requires a title, a file, an image, and an admin_note
    Versionable, Addressible + image and file
    """

    help = {
        'credit': "Item credit",
        'caption': "Item caption",
        'alt':"Alt text",
        'clean_filename_on_upload':"Clean the filename on upload"
    }
    
    credit = models.CharField(_("Credit"), max_length=255, blank=True,
        help_text=help['credit'])
    caption = models.TextField(_("Caption"), blank = True,
        help_text=help['caption'] )
    alt = models.CharField(_("Alt Text"), max_length=255, blank=True,
        help_text=help['alt'])
    clean_filename_on_upload = models.BooleanField( 
        _("Clean filename on upload"), default = True, 
        help_text=help['clean_filename_on_upload'] )

    

    

    def get_alt(self):
        if self.alt:
            return self.alt
        return self.title

    def get_variant_url(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.url
        except:
            return None 

    def get_variant_width(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.width
        except:
            return None  


    def get_variant_height(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.height
        except:
            return None  
    

    def get_variant_link(self, variant_name):
        try:
            field = getattr(self, variant_name)
            gussied_name = variant_name.replace("_", " ").title()
            
            return '<a href="%s" data-img="%s" data-alt="%s" data-credit="%s" data-caption="%s">%s (%spx x %spx)</a><br />'\
                %(field.url, field.url, self.get_alt(), self.credit, self.caption, gussied_name, field.width, field.height)
        except:
            return ''

    def save(self, *args, **kwargs):

        
        #Use filename for title if not specified.
        if self.file and not self.title:
            self.title = clean_path(self.file.url)

        super(RichContentAtom, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.title:
            return ("%s :: %s")%(self.__class__.__name__, self.title)
        elif self.caption or self.credit:
            return ("%s :: %s %s")%(self.__class__.__name__, self.caption, self.credit)
        else:
            return ("%s :: %s")%(self.__class__.__name__, self.pk)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", "credit__icontains","caption__icontains",'admin_note__icontains')

    class Meta:
        abstract = True        




class ImageMolecule( RichContentAtom, VersionableAtom, AddressibleAtom ):

    try:
        image = models.ImageField(upload_to=title_file_name, blank=True, null=True,storage=get_storage('BaseImage'))
    except:
        image = models.ImageField(upload_to=title_file_name, blank=True, null=True)

    # -- Variations
    thumbnail_jpg = ImageSpecField( source='image', format='JPEG', 
        processors=[ResizeToFit(settings.IMAGE_THUMBNAIL_WIDTH, 
        settings.IMAGE_THUMBNAIL_HEIGHT)], 
        options={'quality': settings.IMAGE_THUMBNAIL_QUALITY})
    thumbnail_png = ImageSpecField( source='image', format='PNG', 
        processors=[ResizeToFit(settings.IMAGE_THUMBNAIL_WIDTH, 
        settings.IMAGE_THUMBNAIL_HEIGHT)],
        options={'quality': settings.IMAGE_THUMBNAIL_QUALITY})

    use_png = models.BooleanField( default = False, 
        verbose_name='Use .PNG (instead of .JPG)')

    class Meta:
        abstract = True

    @property
    def file(self):
        return self.image  

    @property
    def thumbnail(self):
        if self.use_png:
            return self.thumbnail_png  
        else:
            return self.thumbnail_jpg

    variants = ('thumbnail',)

class SecureImageMolecule( RichContentAtom, VersionableAtom, AddressibleAtom ):

    try:
        image = models.ImageField(upload_to=title_file_name, blank=True, null=True,storage=get_storage('BaseSecureImage'))
    except:
        image = models.ImageField(upload_to=title_file_name, blank=True, null=True)

    # -- Variations
    thumbnail_jpg = ImageSpecField( source='image', format='JPEG', 
        processors=[ResizeToFit(settings.IMAGE_THUMBNAIL_WIDTH, 
        settings.IMAGE_THUMBNAIL_HEIGHT)], 
        options={'quality': settings.IMAGE_THUMBNAIL_QUALITY})
    thumbnail_png = ImageSpecField( source='image', format='PNG', 
        processors=[ResizeToFit(settings.IMAGE_THUMBNAIL_WIDTH, 
        settings.IMAGE_THUMBNAIL_HEIGHT)],
        options={'quality': settings.IMAGE_THUMBNAIL_QUALITY})

    use_png = models.BooleanField( default = False, 
        verbose_name='Use .PNG (instead of .JPG)')

    class Meta:
        abstract = True

    @property
    def file(self):
        return self.image  

    @property
    def thumbnail(self):
        if self.use_png:
            return self.thumbnail_png  
        else:
            return self.thumbnail_jpg

    variants = ('thumbnail',)    
    
    

class MediaMolecule( ImageMolecule ):

    class Meta:
        abstract = True

    try:
        file = models.FileField(upload_to=title_file_name, blank=True, null=True,storage=get_storage('BaseMedia'))
    except:
        file = models.FileField(upload_to=title_file_name, blank=True, null=True)

class SecureMediaMolecule( SecureImageMolecule ):

    class Meta:
        abstract = True

    try:
        file = models.FileField(upload_to=title_file_name, blank=True, null=True,storage=get_storage('BaseSecureMedia'))
    except:
        file = models.FileField(upload_to=title_file_name, blank=True, null=True)        

