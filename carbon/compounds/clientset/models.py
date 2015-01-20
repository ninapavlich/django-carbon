from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.access import *
from carbon.atoms.models.content import *
from carbon.atoms.models.media import *


class Client(ContentMolecule, AccessibleAtom):
    pass

class ClientMedia(SecureMediaMolecule):
    client = models.ForeignKey('clientset.Client')

class ClientSetItem(OrderedItemMolecule):
    category = models.ForeignKey('clientset.ClientSetCategory')
    item = models.ForeignKey('clientset.ClientMedia')


class ClientSetCategory(CategoryMolecule):
    item_class = ClientSetItem
    class Meta:
        verbose_name_plural = 'Client Set Categories'