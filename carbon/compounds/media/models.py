from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete

from carbon.atoms.models.media import *

from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.admin import AdminThumbnail
from imagekit.processors import ResizeToFill, ResizeToFit

class Image(ImageMolecule):

    variants = ('thumbnail','width_1200', 'width_1200_fill')

    width_1200 = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFit(1200, None, False)], options={'quality': 90})

    width_1200_fill = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFill(1200, None)], options={'quality': 90})


class Media(MediaMolecule):
    pass

class SecureImage(SecureImageMolecule):

    variants = ('thumbnail','width_1200', 'width_1200_fill')

    width_1200 = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFit(1200, None, False)], options={'quality': 90})

    width_1200_fill = ImageSpecField( source='image', format='PNG',
        processors=[ResizeToFill(1200, None)], options={'quality': 90})


class SecureMedia(SecureMediaMolecule):
    pass


@receiver(pre_delete, sender=Image, dispatch_uid='image_delete_signal')
def on_delete_image(sender, instance, using, **kwargs):
    instance.image.delete(save=False)  

@receiver(pre_delete, sender=SecureImage, dispatch_uid='secure_image_delete_signal')
def on_delete_secure_image(sender, instance, using, **kwargs):
    instance.image.delete(save=False)  

@receiver(pre_delete, sender=Media, dispatch_uid='media_delete_signal')
def on_delete_media(sender, instance, using, **kwargs):
    instance.file.delete(save=False)  

@receiver(pre_delete, sender=SecureMedia, dispatch_uid='secure_media_delete_signal')
def on_delete_secure_media(sender, instance, using, **kwargs):
    instance.file.delete(save=False) 