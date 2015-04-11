from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from bs4 import BeautifulSoup

from carbon.utils.slugify import unique_slugify
from carbon.atoms.models.abstract import *
from carbon.atoms.models.content import *

#TODO
# class ContentBlock():
#     pass

class Page(HierarchicalAtom, ContentMolecule):

    tags = models.ManyToManyField('page.PageTag', null=True, blank=True)

    def get_url_path(self):
        path = self.path
        if path.startswith('/'):
            path = path[1:]

        # if path.endswith('/'):
        #     path = path[:1]
            
        return path

    def get_absolute_url(self):
        if self.is_external:
            return self.path_override
        return reverse_lazy('page_page', kwargs = {'path': self.get_url_path() })   

    class Meta:
        abstract = True



class PageTag(TagMolecule):  
    publish_by_default = True

    class Meta:
        verbose_name_plural = 'Page Tags'

    def get_absolute_url(self):
        if self.is_external:
            return self.path_override
        return reverse_lazy('page_tag', kwargs = {'path': self.get_url_path() })   

    def get_children(self):
        all_children = Page.objects.filter(tags__in=[self])
        return [child for child in all_children if child.is_published()]

    class Meta:
        abstract = True
       