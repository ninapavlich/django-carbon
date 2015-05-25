import os
import time
import traceback

from django.db import models
from django.db.models.signals import pre_delete
from django.conf import settings
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.utils.module_loading import import_by_path
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

import boto
from boto.s3.connection import S3Connection, Bucket, Key

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from .abstract import *
from .content import HasImageAtom


#HELPER FUNCTIONS

# bucket = conn.create_bucket(settings.AWS_STORAGE_BUCKET_NAME)
#             k = boto.s3.key.Key(bucket)
#             k.key = settings.MEDIA_DIRECTORY + self.private_file
#             k.set_acl('private')

def is_incremented_file(original, updated):
    """
    Return True if files are incremented versions of eachother: avatar.png, avatar-1.png, avatar-436.png
    """
    try:
        original_path_pieces = original.split(".")
        updated_path_pieces = updated.split(".")

        original_path_start = original_path_pieces[0].split("-")
        updated_path_start = updated_path_pieces[0].split("-")
        # print 'original_path_start: %s updated_path_start: %s'%(original_path_start, updated_path_start)

        are_same_start_path = original_path_start[0] == updated_path_start[0]
        # print 'are_same_start_path? %s == %s? %s'%(original_path_start[0], updated_path_start[0], are_same_start_path)
        if are_same_start_path==False:
            return False

        original_is_integer = True if len(original_path_start)==1 else isinstance( int(original_path_start[1]), int )
        updated_is_integer = True if len(updated_path_start)==1 else isinstance( int(updated_path_start[1]), int )
        increments_are_integers = original_is_integer and updated_is_integer

        # print 'increments_are_integers? %s , %s? %s'%(original_is_integer, updated_is_integer, increments_are_integers)
        if increments_are_integers==False:
            return False

        return True

    except:
        return False

def _media_file_name( instance, filename, file_attribute_name, folder, model_name ):
    
    file, extension = os.path.splitext( filename )
    media_file = getattr(instance, file_attribute_name)

    if instance.clean_filename_on_upload:
        
        filename     = "%s%s"%(slugify(file[:245]), extension)
        filename     = filename.lower()

    full_path = '/'.join( [ folder, filename ] )
    exists = media_file.storage.exists(full_path)

    #If we are changing the image, delete the previous image:
    if instance.pk:
        media_model = get_model(model_name.split('.')[0], model_name.split('.')[1])
        current_instance = media_model.objects.get(pk=instance.pk)
        current_path = str(current_instance.image)

        if full_path != current_path:
            if is_incremented_file(full_path, current_path) == False:
                # print 'Delete previous media: %s'%(current_path)
                current_media_file = getattr(current_instance, file_attribute_name)
                current_media_file.storage.delete(current_path)

    
    #Handle case if file of the same name already exists
    if exists:
        if instance.allow_overwrite==True:
            # print 'Delete media with same name: %s'%(full_path)
            media_file.storage.delete(full_path)
        else:
            counter = 1
            starting_path = full_path
            while exists == True:
                counter += 1
                full_path = starting_path.replace(extension, '-%s%s'%(counter, extension))
                exists = media_file.storage.exists(full_path)
            # print 'Increment filename to get unique: %s'%(full_path)

    

    return full_path        


def image_file_name( instance, filename ):
    
    subfolder = (instance.__class__.__name__).lower()
    full_path = _media_file_name(instance, filename, 'image', subfolder, settings.IMAGE_MODEL)
    return full_path

def media_file_name( instance, filename ):
    
    subfolder = (instance.__class__.__name__).lower()
    full_path = _media_file_name(instance, filename, 'file', subfolder, settings.IMAGE_MODEL)
    return full_path    

def title_file_name( instance, filename ):
    
    return image_file_name(instance, filename)


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



def displaybytes(bytes):
    if bytes < 1024:
        return "%sB"%(bytes)
    kb = (bytes / 1024)
    if kb < 1024:
        return '%sKB'%(kb)

    mb = (kb / 1024)
    if mb < 1024:
        return '%sMB'%(mb)

    gb = (mb / 1024)
    return '%sGB'%(gb)



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
        'credit': "Credit",
        'caption': "Caption",
        'clean_filename_on_upload':"This removes spaces, special characters, and \
            capitalization from the file name for more consistent naming.",
        'allow_overwrite':"Allow file to write over an existing file if the name \
            is the same. If not, we'll automatically add a numerical suffix to \
            ensure file doesn't override existing files.",
        'size':'File size in bytes'
    }
    
    credit = models.CharField(_("Credit"), max_length=255, blank=True,
        help_text=help['credit'])
    caption = models.TextField(_("Caption"), blank = True,
        help_text=help['caption'] )
    clean_filename_on_upload = models.BooleanField( 
        _("Clean filename on upload"), default = True, 
        help_text=help['clean_filename_on_upload'] )
    allow_overwrite = models.BooleanField( 
        _("Allow Overwrite"), default = True, 
        help_text=help['allow_overwrite'] )

    
    size = models.BigIntegerField(null=True, blank=True, help_text=help['size'])
    display_size = models.CharField(_("Display Size"), max_length=255, blank=True, null=True)  

    

    



    def save(self, *args, **kwargs):

        
        #Use filename for title if not specified.
        if self.file and not self.title:
            self.title = clean_path(self.file.url)

        if self.file:
            self.size = self.file.size
            self.display_size = displaybytes(self.file.size)
        else:
            self.size = None
            self.display_size = None

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




class BaseImageMolecule( RichContentAtom, VersionableAtom, AddressibleAtom ):

    help = {
        'alt':"Alt text (very important for SEO)",
        'use_png':"Render image as png instead of jpg when possible"
    }

   
    alt = models.CharField(_("Alt Text"), max_length=255, blank=True,
        help_text=help['alt'])

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
        verbose_name='Use .PNG (instead of .JPG)', help_text=help['use_png'])

    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    

    class Meta:
        abstract = True

    def get_alt(self):
        if self.alt:
            return self.alt
        return self.title

    @property
    def get_format(self):
        if self.use_png:
            return 'PNG'
        return 'JPEG'
    
    @property
    def image_url(self):
        try:
            return self.image.url
        except:
            return None

    @property
    def file(self):
        return self.image  

    @property
    def thumbnail(self):
        if self.use_png:
            return self.thumbnail_png  
        else:
            return self.thumbnail_jpg

    @property
    def thumbnail_url(self):
        try:
            return self.thumbnail.url
        except:
            return ''


    def get_variant_url(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.url
        except Exception, err:
            print traceback.format_exc()

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
    
    def get_variant_link(self, variant_name, include_dimensions=False):
        # try:
        field = getattr(self, variant_name)
        gussied_name = variant_name.replace("_", " ").title()
        
        if variant_name=='image':
            return '<a href="%s" data-img="%s" data-alt="%s" data-credit="%s" data-caption="%s">%s (%spx x %spx)</a>'\
                %(field.url, field.url, self.get_alt(), self.credit, self.caption, 'Original Image', self.image_width, self.image_height)
        
        elif include_dimensions:
            return '<a href="%s" data-img="%s" data-alt="%s" data-credit="%s" data-caption="%s">%s (%spx x %spx)</a>'\
                %(field.url, field.url, self.get_alt(), self.credit, self.caption, gussied_name, field.width, field.height)
        else:
            field_description = ''

            print hasattr(self, 'help')
            print variant_name
            print variant_name in self.help
            print self.help
            
            if hasattr(self, 'help') and variant_name in self.help:
                field_description = ' (%s)'%self.help[variant_name]
            elif hasattr(self, 'help_text') and variant_name in self.help_text:
                field_description = ' (%s)'%self.help_text[variant_name]
            
            return '<a href="%s" data-img="%s" data-alt="%s" data-credit="%s" data-caption="%s">%s%s</a>'\
            %(field.url, field.url, self.get_alt(), self.credit, self.caption, gussied_name, field_description)
        # except:
        #     return ''

    

    def save(self, *args, **kwargs):

        
        if self.image:
            self.image_width = self.image.width
            self.image_height = self.image.height
            self.size = self.image.size
            self.display_size = displaybytes(self.image.size)
        else:
            self.image_width = None
            self.image_height = None
            self.size = None
            self.display_size = None
            

        super(BaseImageMolecule, self).save(*args, **kwargs)


    variants = ('thumbnail',)

class ImageMolecule( BaseImageMolecule ):
    help = {
        'image':"To ensure a precise color replication in image variants, make sure an sRGB color profile has been assigned to each image.",
    }


    try:
        image = models.ImageField(upload_to=image_file_name, blank=True, null=True,storage=get_storage('BaseImage'), help_text=help['image'])
    except:
        image = models.ImageField(upload_to=image_file_name, blank=True, null=True, help_text=help['image'])



    class Meta:
        abstract = True



class SecureImageMolecule( BaseImageMolecule ):
    help = {
        'image':"To ensure a precise color replication in image variants, make sure an sRGB color profile has been assigned to each image.",
    }

    try:
        image = models.ImageField(upload_to=image_file_name, blank=True, null=True,storage=get_storage('BaseSecureImage'), help_text=help['image'])
    except:
        image = models.ImageField(upload_to=image_file_name, blank=True, null=True, help_text=help['image'])

    class Meta:
        abstract = True
    

class MediaMolecule( ImageMolecule ):

    class Meta:
        verbose_name_plural = 'media'
        abstract = True

    try:
        file = models.FileField(upload_to=media_file_name, blank=True, null=True,storage=get_storage('BaseMedia'))
    except:
        file = models.FileField(upload_to=media_file_name, blank=True, null=True)

class SecureMediaMolecule( SecureImageMolecule ):

    class Meta:
        verbose_name_plural = 'secure media'
        abstract = True

    try:
        file = models.FileField(upload_to=media_file_name, blank=True, null=True,storage=get_storage('BaseSecureMedia'))
    except:
        file = models.FileField(upload_to=media_file_name, blank=True, null=True)       


try:
    image_model = settings.IMAGE_MODEL
    @receiver(pre_delete, sender=image_model, dispatch_uid='image_delete_signal')
    def remove_image_file_from_s3(sender, instance, using, **kwargs):
        base_remove_image_file_from_s3(sender, instance, using)
except:
    pass

try:
    secure_image_model = settings.SECURE_IMAGE_MODEL
    @receiver(pre_delete, sender=secure_image_model, dispatch_uid='secure_image_delete_signal')
    def remove_secure_file_from_s3(sender, instance, using, **kwargs):
        base_remove_image_file_from_s3(sender, instance, using)    
except:
    pass

def base_remove_image_file_from_s3(sender, instance, using, **kwargs):
    try:
        delete_file_on_delete = settings.IMAGE_MODEL_DELETE_FILE_ON_DELETE
    except:
        delete_file_on_delete = False

    if delete_file_on_delete:

        #Figure out what bucket to delete
        delete_bucket = None
        if hasattr(instance, 'variants') and instance.variants:
            for variant in instance.variants:
                field = getattr(instance, variant)
                delete_bucket = "/".join(str(field).split('/')[:-1])

            try:
                if delete_bucket:
                    conn = boto.s3.connection.S3Connection(
                        settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)

                    bucket = Bucket(conn, settings.AWS_MEDIA_BUCKET_NAME)

                    for key in bucket.list(prefix=delete_bucket):
                        # print 'delete: %s'%(key)
                        key.delete()               

            except:
                pass

        try:
            instance.image.delete(save=False)  
        except:
            pass

try:
    document_model = settings.DOCUMENT_MODEL
    @receiver(pre_delete, sender=document_model, dispatch_uid='document_delete_signal')
    def remove_document_file_from_s3(sender, instance, using, **kwargs):
        base_remove_document_file_from_s3(sender, instance, using)
except:
    pass

try:
    secure_document_model = settings.SECURE_DOCUMENT_MODEL
    @receiver(pre_delete, sender=secure_document_model, dispatch_uid='secure_document_delete_signal')
    def remove_secure_file_from_s3document_file_from_s3(sender, instance, using, **kwargs):
        base_remove_document_file_from_s3(sender, instance, using)
except:
    pass

def base_remove_document_file_from_s3(sender, instance, using, **kwargs):
    try:
        delete_file_on_delete = settings.DOCUMENT_MODEL_DELETE_FILE_ON_DELETE
    except:
        delete_file_on_delete = False

    if delete_file_on_delete:
        try:
            instance.media_file.delete(save=False)  
        except:
            pass            

 
