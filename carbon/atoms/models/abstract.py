import uuid
import traceback
import sys

from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model



from carbon.utils.slugify import unique_slugify
from carbon.utils.template import get_template_by_pk_or_slug

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

    admin_note = models.TextField(_('admin note'), blank=True, null=True,
        help_text="Not publicly visible")

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super(Versionable, self).save(*args, **kwargs)

    @property
    def edit_item_url(self):
        if self.pk:
            object_type = type(self).__name__
            url = reverse('admin:%s_%s_change' %(self._meta.app_label,  self._meta.model_name),  args=[self.id] )
            return url
        return None

    @property
    def django_id(self):
        return u"%s.%s.%s"%(self._meta.app_label, self._meta.object_name, self.pk)

    def edit_item(self):
        style="style='width:278px;display:block;'"
        if self.pk:            
            try:
                url = self.edit_item_url
                return mark_safe('<a href="%s" %s>Edit Item &gt;</a>'%(url, style))
            except:
                return mark_safe('<span %s>&nbsp;</span>'%(style))
        return mark_safe('<span %s>&nbsp;</span>'%(style))
    

    @property
    def is_edited(self):
        return self.created_date != self.modified_date

    @cached_property
    def abstract_children(self):
        try:
            children = super(VersionableAtom, self).get_children()
        except:
            children = []
        return children


    def get_children(self):
        return self.abstract_children


    @cached_property
    def siblings(self):
        try:
            siblings = super(VersionableAtom, self).get_siblings()
        except:
            siblings = self.__class__.objects.all()
        return siblings

    def get_siblings(self):
        self.siblings

    def is_published(self):
        try:
            published = super(VersionableAtom, self).is_published()
        except:
            published = True
        return published


    def save(self, *args, **kwargs):
        
        self.increment_version_number()

        super(VersionableAtom, self).save(*args, **kwargs)

    def increment_version_number(self):
        self.version = self.version+1

# -- Level 1a
class HierarchicalAtom(models.Model):


    parent = models.ForeignKey('self', blank=True, null=True,
        on_delete=models.SET_NULL)

    @cached_property
    def hierarchical_children(self):
        all_children = self.__class__.objects.filter(parent=self).order_by('order')
        return [child for child in all_children]

    def get_children(self, require_published=True):
        all_children = self.hierarchical_children
        if require_published:
            return [child for child in all_children if child.is_published()]
        return all_children

    @cached_property
    def published_siblings(self):
        if self.parent:
            return self.parent.get_children(True)
        siblings = self.__class__.objects.all()
        return [sibling for sibling in siblings if sibling.is_published()]
        

    @cached_property
    def siblings(self):
        if self.parent:
            return self.parent.get_children()
        return self.__class__.objects.all()

    def get_siblings(self, require_published=True):
        if require_published:
            return self.published_siblings
        else:
            return self.siblings
        

    def get_next_sibling(self, siblings=None, require_published=True):
        if siblings == None:
            siblings = self.get_siblings(require_published)

        if len(siblings)==0:
            return None

        if isinstance(siblings, QuerySet):
            ids = list(siblings.values_list('id', flat=True))
        else:
            ids = [sibling.id for sibling in siblings]

        try:
            index = ids.index(self.id)
        except:
            index = None

        next_item = None
        next_index = None
        if index != None:
            next_index = (index + 1) if index < len(siblings)-1 else None
            
        if next_index != None:
            next_item = siblings[next_index]
        

        return next_item

    def get_previous_sibling(self, siblings=None, require_published=True):
        if siblings == None:
            siblings = self.get_siblings(require_published)

        if len(siblings)==0:
            return None

        if isinstance(siblings, QuerySet):
            ids = list(siblings.values_list('id', flat=True))
        else:
            ids = [sibling.id for sibling in siblings]

        try:
            index = ids.index(self.id)
        except:
            index = None

        previous_item = None
        previous_index = None
        if index != None:
            previous_index = (index -1 ) if index > 0 else None
            
        if previous_index != None:
            previous_item = siblings[previous_index]
        
        return previous_item

    @property
    def edit_parent_url(self):
        if self.parent:
            object_type = type(self.parent).__name__
            return reverse('admin:%s_%s_change' %(self.parent._meta.app_label,  self.parent._meta.model_name),  args=[self.parent.id] )
        return None

    def edit_parent(self):
        style="style='width:278px;display:block;'"
        if self.parent:
            
            try:
                url = self.edit_parent_url
                return mark_safe('<a href="%s" %s>&lt; Edit Parent</a>'%(url, style))
            except:
                return mark_safe('<span %s>&nbsp;</span>'%(style))
        return mark_safe('<span %s>&nbsp;</span>'%(style))
    

    def get_hierarchy(self):
        if self.parent:
            return self.parent.get_hierarchy() + [self]
        return [self]

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
# from django.contrib.contenttypes import generic
# from django.contrib.contenttypes.models import ContentType
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


# -- Level 1.5
class TitleAtom(models.Model):

    help = {
        'title': "The display title for this object.",
        'slug': "Auto-generated page slug for this object.",
    }

    title = models.CharField(_('Title'), max_length=255, 
        help_text=help['title'], blank=True, null=True)

    slug = models.CharField(_('Slug'), max_length=255, blank=True, 
        db_index=True, help_text=help['slug'])

    class Meta:
        abstract = True
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains",)

    def generate_slug(self):
        unique_slugify(self, self.title)
        return self.slug

    def generate_title(self):
        return 'Untitled %s'%(self.__class__.__name__)

    def verify_title_and_slug(self):
        if not self.title:
            self.title = self.generate_title()

        if not self.slug or not self.pk:
            self.slug = self.generate_slug()
        
    def save(self, *args, **kwargs):

        self.verify_title_and_slug()

        super(TitleAtom, self).save(*args, **kwargs)


class OrderedItemAtom(models.Model):

    help = {
        'order': "",
    }

    #When implementing, specify item and tag FKs:
    #tag = models.ForeignKey('app.Model')
    #item = models.ForeignKey('app.Model')
    order = models.IntegerField(default=0, help_text=help['order'])

    class Meta:
        abstract = True  
        ordering = ['order']


# -- Level 2
class AddressibleAtom(TitleAtom):
   
    help = {
        'uuid': "UUID generated for object; can be used for short URLs",
        'parent': "Hierarchical parent of this item. Used to define path.",
        'path': 'Actual path used based on generated and override path',
        'path_generated': "The URL path to this page, based on page hierarchy and slug.",
        'path_override': "The URL path to this page, defined absolutely.",
        'hierarchy': "Administrative Hierarchy",
        'temporary_redirect': "Temporarily redirect to a different path",
        'permanent_redirect': "Permanently redirect to a different path",
        'template': 'Template for view',
        'order': "",
    }
    

    uuid = models.CharField(_('UUID'), max_length=255, blank=True, 
        help_text=help['uuid'])


    order = models.IntegerField(default=0, help_text=help['order']) 
    

    template = models.ForeignKey(settings.TEMPLATE_MODEL, null=True, blank=True,
        help_text=help['template'])    

    path = models.CharField(_('path'), max_length=255, 
        help_text=help['path'], blank=True, null=True)
    title_path = models.CharField(_('title path'), max_length=255, 
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

    @property
    def is_external(self):
        if self.path_override:
            if self.path_override.startswith('/'):
                return False
            return True
        return False

    def get_url_path(self):
        path = self.path
        if path.startswith('/'):
            path = path[1:]

        if path.endswith('/'):
            path = path[:-1]

        return path

    def build_path(self, path_attribute='slug', parent_path_attribute='path'):

        try: 
            model = type(self)
            model._meta.get_field('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            parent_path = getattr(self.parent, parent_path_attribute)
            if parent_path and not parent_path.endswith('/'):
                parent_path = "%s/"%(parent_path)

            
            return "%s%s/" % (parent_path, getattr(self, path_attribute))
        else:
            return "/%s/" % getattr(self, path_attribute)

    def build_hierarchy_path(self):

        try: 
            model = type(self)
            model._meta.get_field('parent')
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
            model._meta.get_field('parent')
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
            model._meta.get_field('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        if has_parent and self.parent:
            return mark_safe("%s&lfloor; %s" % (self.admin_hierarchy_display, self.title))
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

    def get_default_template(self):

        found_template = None

        if hasattr(self, 'default_template') and self.default_template:
            
            found_template = get_template_by_pk_or_slug(self.default_template)

        return found_template

    @property
    def edit_template_url(self):
        if self.template:
            object_type = type(self.template).__name__
            return reverse('admin:%s_%s_change' %(self.template._meta.app_label,  self.template._meta.model_name),  args=[self.template.id] )
        return None

    def edit_template(self):
        style="style='width:278px;display:block;'"
        if self.template:
            
            try:
                url = self.edit_template_url
                return mark_safe('<a href="%s" %s>Edit Template &gt;</a>'%(url, style))
            except:
                return mark_safe('<span %s>&nbsp;</span>'%(style))
        return mark_safe('<span %s>&nbsp;</span>'%(style))
    

    def save(self, *args, **kwargs):
        if not self.template:
            use_default_template = self.get_default_template()
            if use_default_template:
                self.template = use_default_template
        
        try: 
            model = type(self)
            model._meta.get_field('parent')
            has_parent = True 
        except models.FieldDoesNotExist:
            has_parent = False

        #Dont let parent point to self
        if has_parent and self.parent:
            if self.parent == self:
                self.parent = None

        if not self.uuid:
            app_label = type(self)._meta.app_label
            object_name = type(self)._meta.object_name
            self.uuid = "%s.%s.%s"%(app_label, object_name, uuid.uuid1())

        original = None
        if self.pk is not None:
            model = type(self)
            original = model.objects.get(pk=self.pk)
        
        
        self.verify_title_and_slug()

        self.path_generated = self.build_path('slug', 'path')

        self.title_path = self.build_path('title', 'title_path')

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



