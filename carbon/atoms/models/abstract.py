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

    def edit_item(self):
        style="style='width:278px;display:block;'"
        if self.pk:
            
            try:
                object_type = type(self).__name__
                url = reverse('admin:%s_%s_change' %(self._meta.app_label,  self._meta.model_name),  args=[self.id] )
                return '<a href="%s" %s>Edit Item &gt;</a>'%(url, style)
            except:
                return '<span %s>&nbsp;</span>'%(style)
        return '<span %s>&nbsp;</span>'%(style)        

    def get_children(self):
        return []

    def get_siblings(self):
        return []

    def is_published(self):
        return True


    def save(self, *args, **kwargs):
        
        self.increment_version_number()

        super(VersionableAtom, self).save(*args, **kwargs)

    def increment_version_number(self):
        self.version = self.version+1

# -- Level 1a
class HierarchicalAtom(models.Model):


    parent = models.ForeignKey('self', blank=True, null=True,
        related_name="children", on_delete=models.SET_NULL)

    def get_children(self, require_published=True):
        all_children = self.__class__.objects.filter(parent=self).order_by('order')
        if require_published:
            return [child for child in all_children if child.is_published()]
        return all_children

    def get_siblings(self, require_published=True):
        if self.parent:
            return self.parent.get_children(require_published)
        else:
            return []

    def edit_parent(self):
        style="style='width:278px;display:block;'"
        if self.parent:
            
            try:
                object_type = type(self.parent).__name__
                url = reverse('admin:%s_%s_change' %(self.parent._meta.app_label,  self.parent._meta.model_name),  args=[self.parent.id] )
                return '<a href="%s" %s>&lt; Edit Parent</a>'%(url, style)
            except:
                return '<span %s>&nbsp;</span>'%(style)
        return '<span %s>&nbsp;</span>'%(style)

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
        unique=True, db_index=True, help_text=help['slug'])

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

    def save(self, *args, **kwargs):

        if not self.title:
            self.title = 'Untitled %s'%(self.__class__.__name__)

        if not self.slug:
            self.slug = self.generate_slug()

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

    def get_default_template(self):

        found_template = None
        if hasattr(self, 'default_template') and self.default_template:
            
            try:
                app_label = settings.TEMPLATE_MODEL.split('.')[0]
                object_name = settings.TEMPLATE_MODEL.split('.')[1]
                model = get_model(app_label, object_name)

                if isinstance( self.default_template, ( int, long ) ):
                    #try by pk
                    try:
                        found_template = model.objects.get(pk=self.default_template)
                    except:
                        pass

                if found_template == None:
                    #try by slug
                    try:
                        found_template = model.objects.get(slug=self.default_template)
                    except:
                        pass
            except:
                pass

        return found_template

    def edit_template(self):
        style="style='width:278px;display:block;'"
        if self.template:
            
            try:
                object_type = type(self.parent).__name__
                url = reverse('admin:%s_%s_change' %(self.template._meta.app_label,  self.template._meta.model_name),  args=[self.template.id] )
                return '<a href="%s" %s>Edit Template &gt;</a>'%(url, style)
            except:
                return '<span %s>&nbsp;</span>'%(style)
        return '<span %s>&nbsp;</span>'%(style)
    

    def save(self, *args, **kwargs):
        if not self.template:
            use_default_template = self.get_default_template()
            if use_default_template:
                self.template = use_default_template



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

    
