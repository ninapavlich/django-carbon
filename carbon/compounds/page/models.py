from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.abstract import VersionableAtom, HierarchicalAtom
from carbon.atoms.models.content import ContentMolecule, CategoryMolecule, OrderedItemMolecule

class Template(VersionableAtom ):

    help = {
        'content': "",
        'title':"",
    }

    title = models.CharField(_('Page Title'), max_length=255, 
        help_text=help['title'])
    content = models.TextField(_('content'), help_text=help['content'])


    def __unicode__(self):
        return self.title


class Page(HierarchicalAtom, ContentMolecule):

    template = models.ForeignKey('page.Template')

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")



class PageCategoryItem(OrderedItemMolecule):
    category = models.ForeignKey('page.PageCategory')
    item = models.ForeignKey('page.Page')


class PageCategory(CategoryMolecule):
    item_class = PageCategoryItem

    class Meta:
        verbose_name_plural = 'Page Categories'

