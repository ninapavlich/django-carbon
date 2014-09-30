from ..models import *
from ..core.models import Tag as AbstractTag
from ..core.models import TagItemOrder as AbstractTagItemOrder
from ..core.models import Image as AbstractImage


class Client(AbstractTag):
  pass

class ImageSet(AbstractTag):
    pass

class ImageSetOrder(AbstractTagItemOrder):
	pass

class Image(AbstractImage):
	pass