from django.contrib import admin
from django.core.urlresolvers import reverse

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from reversion.admin import VersionAdmin

from .forms import PageAdminForm, PageContentBlockAdminForm, GlobalContentBlockAdminForm

from django_inline_wrestler.admin import TabularInlineOrderable



class PageAdmin(VersionAdmin, HierarchicalContentAdmin):
    form = PageAdminForm

    autocomplete_lookup_fields = HierarchicalContentAdmin.autocomplete_lookup_fields
    
    m2m_fields_list = list(autocomplete_lookup_fields['m2m'])
    # m2m_fields_list.insert(0, 'tags')
    autocomplete_lookup_fields['m2m'] = tuple(m2m_fields_list)

    raw_id_fields = HierarchicalContentAdmin.raw_id_fields
    raw_id_fields_list = list(raw_id_fields)
    # raw_id_fields_list.insert(0, 'tags')
    raw_id_fields = tuple(raw_id_fields_list)

    core_fields = HierarchicalContentAdmin.core_fields
    core_fields_list = list(core_fields)
    # core_fields_list.insert(5, 'tags')
    core_fields = tuple(core_fields_list)

    path_fields = BaseContentAdmin.path_fields
    publication_fields = BaseContentAdmin.publication_fields
    seo_fields = BaseContentAdmin.seo_fields
    social_fields = BaseContentAdmin.social_fields
    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Path", {
            'fields': path_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Publication", {
            'fields': publication_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Search Engine Optimization", {
            'fields': seo_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Social Integration", {
            'fields': social_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    # list_display = ( "parent", "admin_hierarchy", "hierarchy", "path",  "title", "publication_status",)

class PageContentBlockInline(admin.StackedInline):

    form = PageContentBlockAdminForm
    sortable_field_name = "order"
    extra = 0
    
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    meta_fields = BaseVersionableAdmin.meta_fields

    
    core_fields = (
        ('order','title','slug'),
        ('content',),
    )
    additional_fields = (
        ('synopsis'),
        ('publication_status', 'publication_date'),
        ('publish_on_date', 'expire_on_date')
    )

    fieldsets = (
        ("Content", {
            'fields': core_fields
        }),
        ("Additional Properties", {
            'fields': additional_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
    )

    readonly_fields = BaseVersionableAdmin.readonly_fields


class PageTagAdmin(BaseTagAdmin):
    pass


class MenuItemInline(TabularInlineOrderable):
    #model = MenuItem    

    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': [],
    }
    fields = ('order','title','content_type', 'object_id','path_override','edit_item',)
    readonly_fields = BaseVersionableAdmin.readonly_fields + ('path','edit_item',)
    extra = 0







class GlobalContentBlockAdmin(BaseVersionableTitleAdmin):
    #VersionableAtom, TitleAtom, ContentAtom, PublishableAtom

    form = GlobalContentBlockAdminForm

    
    core_fields = BaseVersionableTitleAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.append('content')
    core_fields = tuple(core_fields_list)

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




# admin.site.register(Page, PageAdmin)
# admin.site.register(PageTag, PageTagAdmin)
