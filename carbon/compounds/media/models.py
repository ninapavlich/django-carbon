from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.media import *


class Image(ImageMolecule):
    pass

class Media(MediaMolecule):
	pass

class SecureImage(SecureImageMolecule):
    pass

class SecureMedia(SecureMediaMolecule):
	pass
