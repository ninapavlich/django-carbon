from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.content import *

class Tag(TagMolecule):
    class Meta:
        abstract = True

class Category(CategoryMolecule):
    class Meta:
        abstract = True

class Article(ContentMolecule):
    class Meta:
        abstract = True
  
    tags = models.ManyToManyField('blog.Tag', blank=True, null=True)
    category = models.ForeignKey('blog.Category', blank=True, null=True, 
        on_delete=models.SET_NULL)