from django.db import models
from django.conf import settings

from carbon.compounds.clientset.models import Client as BaseClient
from carbon.compounds.clientset.models import ClientMedia as BaseClientMedia
from carbon.compounds.clientset.models import ClientSetItem as BaseClientSetItem
from carbon.compounds.clientset.models import ClientSetCategory as BaseClientSetCategory

class Client(BaseClient):
    pass

class ClientMedia(BaseClientMedia):
    pass

class ClientSetItem(BaseClientSetItem):
    pass

class ClientSetCategory(BaseClientSetCategory):
    pass