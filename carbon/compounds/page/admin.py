from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from .models import *
from .forms import *




class PageAdmin(HierarchicalContentAdmin):
    form = PageAdminForm

    autocomplete_lookup_fields = HierarchicalContentAdmin.autocomplete_lookup_fields
    
    m2m_fields_list = list(autocomplete_lookup_fields['m2m'])
    m2m_fields_list.insert(0, 'tags')
    autocomplete_lookup_fields['m2m'] = tuple(m2m_fields_list)

    raw_id_fields = HierarchicalContentAdmin.raw_id_fields
    raw_id_fields_list = list(raw_id_fields)
    raw_id_fields_list.insert(0, 'tags')
    raw_id_fields = tuple(raw_id_fields_list)

    core_fields = HierarchicalContentAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(5, 'tags')
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



class PageTagAdmin(BaseTagAdmin):
    pass


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': [],
    }


    fields = ('order','title',  'content_type', 'object_id', 'path_override', 'target', 'publication_status', 'publish_on_date', 'expire_on_date')


    sortable_field_name = 'order'
    extra = 0


class MenuItemAdmin(BaseVersionableAdmin):

    
    core_fields = (
        'title',
        'slug',
        'publication_status'
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("hierarchy",)

    list_display = ( "admin_hierarchy", "title",'publication_status')
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

    inlines = [MenuItemInline]



admin.site.register(Page, PageAdmin)
admin.site.register(PageTag, PageTagAdmin)
admin.site.register(MenuItem, MenuItemAdmin)