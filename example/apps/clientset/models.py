from django.db import models
from django.conf import settings

from carbon.compounds.clientset.models import Client as BaseClient
from carbon.compounds.clientset.models import ClientMedia as BaseClientMedia
from carbon.compounds.clientset.models import ClientSetItem as BaseClientSetItem
from carbon.compounds.clientset.models import ClientSetCategory as BaseClientSetCategory

class Client(BaseClient):
    pass

class ClientMedia(BaseClientMedia):
    client = models.ForeignKey('clientset.Client')

class ClientSetItem(BaseClientSetItem):
    category = models.ForeignKey('clientset.ClientSetCategory')
    item = models.ForeignKey('clientset.ClientMedia')

class ClientSetCategory(BaseClientSetCategory):
    item_class = ClientSetItem