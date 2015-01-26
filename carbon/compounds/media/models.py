from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete

from carbon.atoms.models.media import *


class Image(ImageMolecule):
    pass

class Media(MediaMolecule):
	pass

class SecureImage(SecureImageMolecule):
    pass

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