from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.content import *
from carbon.atoms.models.media import *

class Client(TagMolecule):
  pass

class ClientImageSet(CategoryMolecule):
    client = models.ForeignKey('gallery.Client', 
        blank=True, null=True)

class ClientImage(SecureImageMolecule):
	pass