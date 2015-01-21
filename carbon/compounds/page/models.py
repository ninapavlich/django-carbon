from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.abstract import VersionableAtom, HierarchicalAtom
from carbon.atoms.models.content import ContentMolecule, TagMolecule

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
    tags = models.ManyToManyField('page.PageTag')

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")



class PageTag(TagMolecule):  

    class Meta:
        verbose_name_plural = 'Page Tags'

