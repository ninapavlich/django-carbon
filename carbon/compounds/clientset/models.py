from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.access import *
from carbon.atoms.models.content import *
from carbon.atoms.models.media import *


class Client(ContentMolecule, AccessibleAtom):
    class Meta:
        abstract = True

class ClientMedia(SecureMediaMolecule):

    # YOU MUST IMPLEMENT THIS:
    # client = models.ForeignKey('clientset.Client')

    class Meta:
        abstract = True

class ClientSetItem(OrderedItemMolecule):

    # YOU MUST IMPLEMENT THIS:
    # category = models.ForeignKey('clientset.ClientSetCategory')
    # item = models.ForeignKey('clientset.ClientMedia')

    class Meta:
        abstract = True


class ClientSetCategory(CategoryMolecule):
    # YOU MUST IMPLEMENT THIS:
    # item_class = ClientSetItem
    class Meta:
        abstract = True
        verbose_name_plural = 'Client Set Categories'        