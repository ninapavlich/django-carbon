from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from reversion.admin import VersionAdmin
from django_inline_wrestler.admin import TabularInlineOrderable

from carbon.atoms.admin.content import BaseVersionableAdmin, BaseVersionableTitleAdmin

# from .models import *
from .forms import *



class TemplateAdmin(VersionAdmin, BaseVersionableAdmin):
    
    form = TemplateAdminForm
    prepopulated_fields = {"slug": ("title",)}

    core_fields = (
        ('title','slug'),
        'file_template',
        'custom_template',
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )    


class BaseFrontendPackageAdmin(VersionAdmin, BaseVersionableTitleAdmin):

    prepopulated_fields = {"slug": ("title",)}
    core_fields = (
        ('title','slug'),
        ('source','minified'),
        ('file_source', 'file_minified'),
    )
    meta_fields = BaseVersionableTitleAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    ) 
    #readonly_fields = BaseVersionableTitleAdmin.readonly_fields + ('file_source','file_minified')

class CSSPackageAdmin(BaseFrontendPackageAdmin):
    pass

class JSPackageAdmin(BaseFrontendPackageAdmin):
    pass    



class BaseFrontendResourceAdmin(VersionAdmin, BaseVersionableTitleAdmin):

    prepopulated_fields = {"slug": ("title",)}
    core_fields = (
        ('edit_parent',),
        ('title','slug'),
        ('compiler',),
        ('file_source_url'),        
    )
    source_fields = (
        'custom_source',
    )
    meta_fields = BaseVersionableTitleAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Source", {
            'fields': source_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    ) 
    readonly_fields = BaseVersionableTitleAdmin.readonly_fields + ('edit_parent',)

class CSSResourceAdmin(BaseFrontendResourceAdmin):
    form = CSSResourceAdminForm

class JSResourceAdmin(BaseFrontendResourceAdmin):
    form = JSResourceAdminForm

class BaseFrontendResourceInline(admin.StackedInline):
    #fields = ('order','title', 'compiler','file_source_url','edit_item',)
    readonly_fields = BaseVersionableTitleAdmin.readonly_fields + ('edit_item',)
    ordering = ("order",)
    sortable_field_name = 'order'
    core_fields = (
        ('title','slug', 'order', 'edit_item'),
        ('compiler', 'file_source_url', 'file_source_path'),
    )
    source_fields = (
        'custom_source',
    )
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Source", {
            'fields': source_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
    ) 
    classes = ('grp-collapse grp-open',)
    prepopulated_fields = {"slug": ("title",)}
    
    extra = 0

class CSSResourceInline(BaseFrontendResourceInline):
    form = CSSResourceAdminForm
    prepopulated_fields = {"slug": ("title",)}

class JSResourceInline(BaseFrontendResourceInline):
    form = JSResourceAdminForm
    prepopulated_fields = {"slug": ("title",)}
    
# admin.site.register(Template, TemplateAdmin)