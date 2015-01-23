from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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


class Menu(VersionableAtom):

    help = {
        'title': "",
        'slug': "",
    }

    title = models.CharField(_('Title'), max_length=255, 
        help_text=help['title'])

    slug = models.CharField(_('Slug'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])


class MenuItem(VersionableAtom):

    help = {
        'title': "",
        'slug': "",
        'path': "Override path for this menu item",
        'target': "",
        'order':""
    }

    BLANK = '_blank'
    SELF = '_self'
    PARENT = '_parent'
    TOP = '_top'
    TARGET_CHOICES = (
        (BLANK, _(BLANK)),
        (SELF, _(SELF)),
        (PARENT, _(PARENT)),
        (TOP, _(TOP))        
    )

    parent = models.ForeignKey('page.Menu')

    title = models.CharField(_('Title'), max_length=255, help_text=help['title'])

    order = models.IntegerField(default=0, help_text=help['order'])

    #Point to an object
    try:
        content_type = models.ForeignKey(ContentType, 
            limit_choices_to={"model__in": settings.MENU_MODEL_CHOICES})
    except:
        content_type = models.ForeignKey(ContentType)

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    #Point to an explicit path
    path = models.CharField(_('Path'), max_length=255, help_text=help['path'], 
        blank=True, null=True)

    target = models.CharField(_('Target'), max_length=255, help_text=help['target'], 
        choices=TARGET_CHOICES, default=SELF)

    def get_path(self):
        if self.content_object:
            if hasattr(self.content_object, 'get_absolute_url'):
                return self.content_object.get_absolute_url()
        
        return self.path

    def get_link(self):
        '<a href="%s" target="%s">%s</a>'%(self.get_path, self.target, self.title)
