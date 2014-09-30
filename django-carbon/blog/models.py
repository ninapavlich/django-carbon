from ..models import *
from ..core.models import Tag as AbstractTag
from ..core.models import TagItemOrder as AbstractTagItemOrder
from ..core.models import Article as AbstractArticle
from ..core.models import Image as AbstractImage
from ..core.models import Document as AbstractDocument
from ..core.models import Location as AbstractLocation

class Image(AbstractImage):
    pass

class Document(AbstractDocument):
  pass

class Location(AbstractLocation):
  pass

class Tag(AbstractTag):
    pass

class TagItemOrder(AbstractTagItemOrder):
  pass

class Article(AbstractArticle):
  pass