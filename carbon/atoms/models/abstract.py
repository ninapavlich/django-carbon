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


from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

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
        'path': "The URL path to this page, based on page heirarchy and slug.",
        'path_override': "The URL path to this page, defined absolutely.",
        'temporary_redirect': "Temporarily redirect to a different path",
        'permanent_redirect': "Permanently redirect to a different path",
        'order': "Simple order of item. ",
    }
    

    title = models.CharField(_('Page Title'), max_length=255, 
        help_text=help['title'])

    slug = models.CharField(_('Text ID'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])
    uuid = models.CharField(_('UUID'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])

    
    order = models.IntegerField(default=0, help_text=help['order'])

    path = models.CharField(_('path'), max_length=255, unique=True,
        help_text=help['path'])
    path_override = models.CharField(_('path override'), max_length=255,
        unique=True, help_text=help['path_override'])

    temporary_redirect = models.CharField(_('Temporary Redirect'), max_length=255,
        blank=True, help_text=help['temporary_redirect'])
    permanent_redirect = models.CharField(_('Permanent Redirect'), max_length=255,
        blank=True, help_text=help['permanent_redirect'])


    class Meta:
        abstract = True

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

    def build_path(self):

        try: 
            self.model._meta.get_field_by_name('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            return "%s%s/" % (self.parent.path, self.slug)
        else:
            return "/%s/" % self.slug

    def generate_slug(self):
        raise NotImplementedError('Class should specify generate_slug function')

    def get_absolute_url(self):
        return self.path
    

    def save(self, *args, **kwargs):

        new_path = self.build_path()

        #If path has changed, notify children
        if self.path != new_path:
            self.path = new_path
            [p.save() for p in self.get_children()]

        if not self.slug:
            self.slug = self.generate_slug()

        if not self.uuid:
            app_label = type(self)._meta.app_label
            object_name = type(self)._meta.object_name
            self.uuid = "%s.%s.%s"%(app_label, object_name, uuid.uuid1())
            print "Set UUID: %s"%(self.uuid)

        super(Addressible, self).save(*args, **kwargs)
