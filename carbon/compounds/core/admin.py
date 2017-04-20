from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe

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

    search_fields = ('title', 'slug', 'admin_note', 'custom_template')
    list_display = ('title', 'slug')


class BaseFrontendPackageAdmin(VersionAdmin, BaseVersionableTitleAdmin):

    def archived_versions(self, obj):
        url = obj.get_archived_file_url(obj.version, True)
        return mark_safe("You can download archived versions using this URL schema:<br /><a href='%s' target='_blank'>%s</a>"%(url, url))
    

    def rerender(modeladmin, request, queryset):
        for object in queryset:
            object.render(True, True)
            if object.error_source_content == None:
                messages.add_message(request, messages.SUCCESS, 'Package %s was re-rendered'%(object.title))
            else:
                messages.add_message(request, messages.ERROR, 'An error was encountered when rendering %s: %s'%(object.title, object.error_source_content))

    rerender.short_description = "Re-Render Package"

    prepopulated_fields = {"slug": ("title",)}
    core_fields = (
        ('title','slug'),
        # ('source','minified'),
        ('file_source', 'file_minified'),
    )
    info_fields = (
        ('version','peg_revision',),
        'archived_versions',
        'error_source_content',
        'needs_render'
    )
    meta_fields = BaseVersionableTitleAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Info", {
            'fields': info_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    ) 
    #readonly_fields = BaseVersionableTitleAdmin.readonly_fields + ('file_source','file_minified')

    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "error_source_content", "archived_versions"
    ) 

    actions = [rerender]


    def response_change(self, request, object):
        response = super(BaseFrontendPackageAdmin, self).response_change(request, object)
        object.render()

        if object.error_source_content != None:
            messages.add_message(request, messages.ERROR, 'An error was encountered when rendering %s: %s'%(object.title, object.error_source_content))

        return response

    def response_add(self, request, object):
        response = super(BaseFrontendPackageAdmin, self).response_add(request, object)
        object.render()

        if object.error_source_content != None:
            messages.add_message(request, messages.ERROR, 'An error was encountered when rendering %s: %s'%(object.title, object.error_source_content))

        return response



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

    def edit_item(self, obj):
        return mark_safe("<a href='%s' target='_blank'>See Item Details and Revision History></a>"%(obj.edit_item_url))
    
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
            'classes': ( 'grp-collapse grp-open', )
        }),
    ) 
    classes = ('grp-collapse grp-open',)
    prepopulated_fields = {"slug": ("title",)}
    
    extra = 0

class CSSResourceInline(BaseFrontendResourceInline):
    form = CSSResourceAdminForm
    fk_name = 'parent'
    prepopulated_fields = {"slug": ("title",)}

class JSResourceInline(BaseFrontendResourceInline):
    form = JSResourceAdminForm
    fk_name = 'parent'
    prepopulated_fields = {"slug": ("title",)}

    core_fields = (
        ('title','slug', 'order', 'edit_item'),
        ('file_source_url', 'file_source_path'),
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
            'classes': ( 'grp-collapse grp-open', )
        }),
    ) 




class MenuItemInline(TabularInlineOrderable):
    #model = MenuItem  
    form = MenuItemForm  
    fk_name = 'parent'
    
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': [],
    }
    fields = ('order','title','content_type', 'object_id','path_override','edit_item',)
    readonly_fields = BaseVersionableAdmin.readonly_fields + ('path','edit_item',)
    extra = 0


class MenuItemAdmin(BaseVersionableAdmin):
            
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': ('parent',),
    }
    raw_id_fields = ( 'parent',)

    core_fields = (
        ('edit_parent','parent'),
        ('title','slug'),
        ('content_type', 'object_id',),
        ('path_override',),
        ('path',),
        ('publication_status','css_classes',),
        ('target','extra_attributes')
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("hierarchy",)

    
    list_display = ( "admin_hierarchy", "title", 'path', 'publication_status')
    list_display_links = ('title',)
    fieldsets = (
        ("Main", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': BaseVersionableAdmin.meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    readonly_fields = BaseVersionableAdmin.readonly_fields + ('path','edit_parent')
    # inlines = [MenuItemInline]

class AdminAppLinkInline(TabularInlineOrderable):

    # model = AdminLinkItem
    fk_name = 'parent'
    ordering = ("order",)
    extra = 0
    fieldsets = (
        ( 'Links', { 'fields': ( 'order', 'model_path', ) } ),
    )

class AdminLinkInline(TabularInlineOrderable):

    # model = AdminLink
    fk_name = 'parent'
    ordering = ("order",)
    extra = 0
    fieldsets = (
        ( 'Links', { 'fields': ( 'order', 'title', 'url') } ),
    )    
  
class AdminAppGroupAdmin(VersionAdmin, BaseVersionableAdmin):
    #inlines = [AdminAppLinkInline]
    core_fields = (
        ('title', 'open_by_default'),
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

    list_display = ('title', 'order',)
    list_editable = ('order',)

class AdminSidebarAdmin(VersionAdmin, BaseVersionableAdmin):
    #inlines = [AdminLinkInline]
    core_fields = (
        ('title',),
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

    list_display = ('title', 'order',)
    list_editable = ('order',)

class LegacyURLRefererInline(admin.TabularInline):
    #model = LegacyURLReferer

    fields = ('referer_title','referer_url', 'created_date')
    extra = 0

    readonly_fields = BaseVersionableAdmin.readonly_fields


class LegacyURLAdmin(BaseVersionableAdmin):

    def visit_old_link(self, obj):
        return mark_safe("<a href='%s%s' target='_blank'>Visit Old Link</a>"%(settings.LEGACY_URL_ARCHIVE_DOMAIN, obj.url))
    

    def test_redirect(self, obj):
        return mark_safe("<a href='%s' target='_blank'>Test Redirect</a>"%(obj.url))
    
    
    core_fields = (
        ('url'),
        ( 'content_type', 'object_id',),
        ('path_override'),
        ('path'),
        ('visit_old_link','test_redirect')
    )
    

    list_display = ( "url", "path",'created_date', )
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': [],
    }

    fieldsets = (
        ("Main", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': BaseVersionableAdmin.meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    readonly_fields = BaseVersionableAdmin.readonly_fields + ('path','visit_old_link','test_redirect')

    # inlines = [LegacyURLRefererInline]    

# admin.site.register(Template, TemplateAdmin)
# admin.site.register(MenuItem, MenuItemAdmin)
# admin.site.register(LegacyURL, LegacyURLAdmin)
