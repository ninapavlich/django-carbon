from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


from carbon.utils.slugify import unique_slugify
from carbon.atoms.models.abstract import VersionableAtom, HierarchicalAtom, AddressibleAtom
from carbon.atoms.models.content import ContentMolecule, TagMolecule, TemplateMolecule, PublishableAtom


class Page(HierarchicalAtom, ContentMolecule):

    # YOU MUST IMPLEMENT THIS:
    # tags = models.ManyToManyField('page.PageTag', null=True, blank=True)

    def get_url_path(self):
        path = self.path
        if path.startswith('/'):
            path = path[1:]

        # if path.endswith('/'):
        #     path = path[:1]
            
        return path

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")

    # YOU MUST IMPLEMENT THIS:
    # def get_absolute_url(self):
    #     return reverse('pages_page', kwargs = {'path': self.get_url_path() })   

    class Meta:
        abstract = True



class PageTag(TagMolecule):  

    class Meta:
        verbose_name_plural = 'Page Tags'

    # YOU MUST IMPLEMENT THIS:
    # def get_absolute_url(self):
    #     return reverse('pages_tag', kwargs = {'path': self.get_url_path() })   

    def get_children(self):
        all_children = Page.objects.filter(tags__in=[self])
        return [child for child in all_children if child.is_published()]

    class Meta:
        abstract = True
        


class MenuItem(VersionableAtom, HierarchicalAtom, AddressibleAtom, PublishableAtom):

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

    
    #Point to an object
    try:
        content_type = models.ForeignKey(ContentType, 
            limit_choices_to={"model__in": settings.MENU_MODEL_CHOICES}, null=True, blank=True)
    except:
        content_type = models.ForeignKey(ContentType, null=True, blank=True)

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


    target = models.CharField(_('Target'), max_length=255, help_text=help['target'], 
        choices=TARGET_CHOICES, default=SELF)

    def get_path(self):
        if self.content_object:
            if hasattr(self.content_object, 'get_absolute_url'):
                return self.content_object.get_absolute_url()
        
        return self.path_override

    def get_link(self):
        '<a href="%s" target="%s">%s</a>'%(self.get_path, self.target, self.title)


    def save(self, *args, **kwargs):

        #Published by default
        if not self.pk:
            self.publication_status = PublishableAtom.PUBLISHED

        super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        abstract = True
    
