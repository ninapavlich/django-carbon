import uuid
import traceback
import sys

from django.db import models
from django.db.models.loading import get_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.safestring import mark_safe

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from carbon.utils.slugify import unique_slugify

# -- Level 1
class VersionableAtom(models.Model):


    version = models.IntegerField(default=0) #THOUGHT: Is this useful??
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_created_by',
        on_delete=models.SET_NULL)

    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_modified_by',
        on_delete=models.SET_NULL)

    admin_note = models.TextField(_('admin note'), blank=True, null=True)

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super(Versionable, self).save(*args, **kwargs)

    

    def save(self, *args, **kwargs):
        
        self.increment_version_number()

        super(VersionableAtom, self).save(*args, **kwargs)

    def increment_version_number(self):
        self.version = self.version+1

# -- Level 1a
class HierarchicalAtom(models.Model):


    parent = models.ForeignKey('self', blank=True, null=True,
        related_name="children", on_delete=models.SET_NULL)

    def get_children(self):
        return self.__class__.objects.filter(parent=self)

    def get_next_child(self, item):
        children = self.get_children()
        next_index = (children.index(item) + 1) % len(children)
        return children[next_index]

    def get_previous_child(self, item):
        children = self.get_children()
        previous_index = (children.index(item) + len(children) - 1) % len(children)
        return children[previous_index]


    class Meta:
        abstract = True

# # -- Level 1b
# class Flat(models.Model):

#     def get_parent_model():
#         raise NotImplementedError('Class should specify parent model')

#     content_type = models.ForeignKey(ContentType, limit_choices_to={"model__in": self.get_parent_model()}))
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')

#     class Meta:
#         abstract = True

#     @property
#     def parent(self):
#         return self.content_object

#     @staticmethod
#     def get_by_parent(search_class, parent):
#         return search_class.objects.filter(object_id=parent.id, content_type=ContentType.objects.get_for_model(parent))




# -- Level 2
class AddressibleAtom(models.Model):
   
    help = {
        'title': "The display title for this object.",
        'slug': "Auto-generated page slug for this object.",
        'uuid': "UUID generated for object; can be used for short URLs",
        'parent': "Hierarchical parent of this item. Used to define path.",
        'path': 'Actual path used based on generated and override path',
        'path_generated': "The URL path to this page, based on page hierarchy and slug.",
        'path_override': "The URL path to this page, defined absolutely.",
        'hierarchy': "Administrative Hierarchy",
        'temporary_redirect': "Temporarily redirect to a different path",
        'permanent_redirect': "Permanently redirect to a different path",
        'order': "Simple order of item. ",
        'template': 'Template for view'
    }
    

    title = models.CharField(_('Title'), max_length=255, 
        help_text=help['title'], blank=True, null=True)

    slug = models.CharField(_('Slug'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])
    uuid = models.CharField(_('UUID'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])

    
    order = models.IntegerField(default=0, help_text=help['order'])


    template = models.ForeignKey(settings.TEMPLATE_MODEL, null=True, blank=True,
        help_text=help['template'])

    

    path = models.CharField(_('path'), max_length=255, 
        help_text=help['path'], blank=True, null=True)
    path_generated = models.CharField(_('generated path'), max_length=255, 
        help_text=help['path_generated'], blank=True, null=True)
    path_override = models.CharField(_('path override'), max_length=255,
        help_text=help['path_override'], blank=True, null=True)
    hierarchy = models.CharField(_('hierarchy'), max_length=255, unique=True,
        null=True, blank=True, help_text=help['hierarchy'])

    temporary_redirect = models.CharField(_('Temporary Redirect'), max_length=255,
        blank=True, help_text=help['temporary_redirect'])
    permanent_redirect = models.CharField(_('Permanent Redirect'), max_length=255,
        blank=True, help_text=help['permanent_redirect'])


    class Meta:
        abstract = True
        ordering = ['hierarchy']

    def __unicode__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains",)

    @staticmethod
    def get_by_uuid(uuid):
        if uuid:
            split = uuid.split('.')
            try:
                app_label = split[0]
                object_name = split[1]
                uuid = split[2]

                model = get_model(app_label, object_name)
                instance = model.objects.get(uuid=uuid)
                return instance
            except Exception, err:
                if settings.DEBUG:
                    print 'Error getting object by uuid %s - %s'%(traceback.format_exc(), sys.exc_info()[0])
        return None

    def get_url_path(self):
        path = self.path
        if path.startswith('/'):
            path = path[1:]

        if path.endswith('/'):
            path = path[:-1]

        return path

    def build_path(self):

        try: 
            model = type(self)
            model._meta.get_field_by_name('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            parent_path = self.parent.path
            if parent_path and not parent_path.endswith('/'):
                parent_path = "%s/"%(parent_path)

            return "%s%s/" % (parent_path, self.slug)
        else:
            return "/%s/" % self.slug

    def build_hierarchy_path(self):

        try: 
            model = type(self)
            model._meta.get_field_by_name('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            return "%s%s/%s/" % (self.parent.build_hierarchy_path(), str(self.order).zfill(4), self.slug)
        else:
            return "/%s/%s/" % (str(self.order).zfill(4), self.slug)

    @property
    def admin_hierarchy_display(self):

        try: 
            model = type(self)
            model._meta.get_field_by_name('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            return "%s<span style='color:#fff'>|------</span>" % self.parent.admin_hierarchy_display
        else:
            return ''

    @property
    def admin_hierarchy(self):

        try: 
            model = type(self)
            model._meta.get_field_by_name('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            return mark_safe("%s&lfloor; %s" % (self.parent.admin_hierarchy_display, self.title))
        else:
            return self.title


    def generate_slug(self):
        unique_slugify(self, self.title)
        return self.slug

    def generate_path(self):
        if self.path_override != None and self.path_override != '':
            return  self.path_override
        return self.path_generated

    def get_absolute_url(self):
        return self.path
    

    def save(self, *args, **kwargs):

        if not self.title:
            self.title = 'Untitled %s'%(self.__class__.__name__)
        
        try: 
            model = type(self)
            model._meta.get_field_by_name('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        #Dont let parent point to self
        if has_parent and self.parent:
            if self.parent == self:
                self.parent = None

        if not self.slug:
            self.slug = self.generate_slug()


        if not self.uuid:
            app_label = type(self)._meta.app_label
            object_name = type(self)._meta.object_name
            self.uuid = "%s.%s.%s"%(app_label, object_name, uuid.uuid1())

        original = None
        if self.pk is not None:
            model = type(self)
            original = model.objects.get(pk=self.pk)
        
            
        self.path_generated = self.build_path()

        
        self.path = self.generate_path()
        self.hierarchy = self.build_hierarchy_path()

        path_has_changed = False
        if original != None:
            if (original.path != self.path):
                path_has_changed = True


        super(AddressibleAtom, self).save(*args, **kwargs)

        #If path has changed, notify children
        if path_has_changed:
            [p.save() for p in self.get_children()]

    
