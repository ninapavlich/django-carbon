import pytz

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete

from carbon.atoms.models.content import TagMolecule, CategoryMolecule
from carbon.atoms.models.media import *

from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.admin import AdminThumbnail
from imagekit.processors import ResizeToFill, ResizeToFit

from imagekit_cropper.processors import PositionCrop, PositionAndFormatCrop, FormatProcessor




class MediaPositionCrop(PositionCrop):
    def get_hash(self):
        #Hash based on crop value
        crop_value = getattr(self.image_instance, self.crop_position_field)
        file_modified_date = getattr(self.image_instance, 'file_modified_date')
        file_modified_timezone = '' if not file_modified_date else file_modified_date
        hashed = u"%s-%s-%s-%s-%s"%(self.crop_position_field, crop_value, self.width, self.height, file_modified_timezone)
        # print hashed
        return hashed


class MediaPositionAndFormatCrop(PositionAndFormatCrop):
    
    def get_hash(self):
        #Hash based on crop value
        crop_value = getattr(self.image_instance, self.crop_position_field)
        file_modified_date = getattr(self.image_instance, 'file_modified_date')
        file_modified_timezone = '' if not file_modified_date else file_modified_date
        format = getattr(self.image_instance, self.format_field)
        hashed = u"%s-%s-%s-%s-%s-%s"%(self.crop_position_field, crop_value, format, self.width, self.height, file_modified_timezone)
        # print hashed
        return hashed

class MediaFormatProcessor(FormatProcessor):
    
    def get_hash(self):
        #Hash based on format value
        file_modified_date = getattr(self.image_instance, 'file_modified_date')
        file_modified_timezone = '' if not file_modified_date else file_modified_date
        format = getattr(self.image_instance, self.format_field)
        hashed = u"%s-%s-%s-%s"%(format, self.width, self.height, file_modified_timezone)
        # print hashed
        return hashed     





class MediaTag(TagMolecule):
    publish_by_default = True
    # default_template = 'media_tag'
    # item_classes = [Image, Media, SecureImage, SecureMedia]
    
    class Meta:
        abstract = True

class MediaFolder(CategoryMolecule):
    publish_by_default = True
    # item_class = None
    # item_classes = None
    # category_property_name = 'folder'

    
    class Meta:
        abstract = True


class Image(ImageMolecule):

    #EXAMPLE VARIANTS
    # variants = ('thumbnail','width_1200', 'width_1200_fill', 'square_600')

    # square_600 = ImageSpecField( source='image', format='PNG',
    #     processors=[ResizeToFill(600, 600)], options={'quality': 85})

    # width_1200 = ImageSpecField( source='image', format='PNG',
    #     processors=[ResizeToFit(1200, None, False)], options={'quality': 85})

    # width_1200_fill = ImageSpecField( source='image', format='PNG',
    #     processors=[ResizeToFit(1200, None)], options={'quality': 85})

    # tags = models.ManyToManyField('media.MediaTag', blank=True, related_name='%(app_label)s_%(class)s_tags')

    class Meta:
        abstract = True

class SecureImage(SecureImageMolecule):

    #EXAMPLE VARIANTS
    # variants = ('thumbnail','width_1200', 'width_1200_fill', 'square_600')

    # square_600 = ImageSpecField( source='image', format='PNG',
    #     processors=[ResizeToFill(600, 600)], options={'quality': 85})

    # width_1200 = ImageSpecField( source='image', format='PNG',
    #     processors=[ResizeToFit(1200, None, False)], options={'quality': 85})

    # width_1200_fill = ImageSpecField( source='image', format='PNG',
    #     processors=[ResizeToFit(1200, None)], options={'quality': 85})

    # tags = models.ManyToManyField('media.MediaTag', blank=True, related_name='%(app_label)s_%(class)s_tags')

    class Meta:
        abstract = True        




class Media(MediaMolecule):

    # tags = models.ManyToManyField('media.MediaTag', blank=True, related_name='%(app_label)s_%(class)s_tags')

    class Meta:
        abstract = True
        verbose_name_plural = 'media'



class SecureMedia(SecureMediaMolecule):

    # tags = models.ManyToManyField('media.MediaTag', blank=True, related_name='%(app_label)s_%(class)s_tags')

    class Meta:
        abstract = True
        verbose_name_plural = 'secure media'




@receiver(pre_delete, sender=Image, dispatch_uid='image_delete_signal')
def on_delete_image(sender, instance, using, **kwargs):
    print 'on delete image test'
    instance.image.delete(save=False)  

@receiver(pre_delete, sender=Media, dispatch_uid='media_delete_signal')
def on_delete_media(sender, instance, using, **kwargs):
    instance.file.delete(save=False)  

@receiver(pre_delete, sender=SecureMedia, dispatch_uid='secure_media_delete_signal')
def on_delete_secure_media(sender, instance, using, **kwargs):
    instance.file.delete(save=False) 

@receiver(pre_delete, sender=SecureImage, dispatch_uid='secure_image_delete_signal')
def on_delete_secure_media(sender, instance, using, **kwargs):
    instance.image.delete(save=False) 