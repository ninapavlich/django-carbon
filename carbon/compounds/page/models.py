from django.db import models
from django.conf import settings
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

        if hasattr(self.__class__, 'detail_view') and self.__class__.detail_view:
            return reverse_lazy(self.__class__.detail_view, kwargs = {'path': self.get_url_path() })   

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
        all_children = self.__class__.objects.filter(parent=self)
        return [child for child in all_children if child.is_published()]

    class Meta:
        abstract = True
       
class PageContentBlock(VersionableAtom, OrderedItemAtom, TitleAtom, ContentAtom, PublishableAtom):
    
    publish_by_default = True

    parent = models.ForeignKey('page.Page', related_name="page_blocks")

    def get_siblings(self, published=True):
        siblings = self.__class__.objects.filter(parent=self.parent)

        if published:
            return [child for child in siblings if child.is_published()]
        else:
            return siblings

    def verify_title_and_slug(self):
        siblings = self.get_siblings(False)

        if not self.title:
            self.title = '%s %s'%(self._meta.verbose_name.title(), len(siblings)+1)

        if not self.slug or not self.pk:
            self.slug = self.generate_slug()

    def generate_slug(self):
        
        siblings = self.get_siblings(False)
        # -- Make sure slug is unique
        if self.slug:
            raw_slug = self.slug
        else:
            raw_slug = self.title

        raw_slug = raw_slug.lower()
        
        unique_slugify(self, raw_slug, 'slug', siblings, "_")

        return self.slug

    class Meta:
        verbose_name = 'Page Block'
        verbose_name_plural = 'Page Blocks'
        ordering = ['order']
        abstract = True


class GlobalContentBlock(VersionableAtom, TitleAtom, ContentAtom, PublishableAtom):
    
    publish_by_default = True


    class Meta:
        verbose_name = 'Global Content Block'
        verbose_name_plural = 'Global Content Blocks'
        abstract = True        
    
    