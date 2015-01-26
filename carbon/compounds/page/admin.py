from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *
from .models import *



class TemplateAdmin(BaseVersionableAdmin):

    autocomplete_lookup_fields = {
        'fk': ('parent', ),
    }
    raw_id_fields = ( 'parent', )

    core_fields = (
        'parent',
        'title',
        'content',
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



class PageAdmin(HierarchicalContentAdmin):

    autocomplete_lookup_fields = HierarchicalContentAdmin.autocomplete_lookup_fields
    fk_fields_list = list(autocomplete_lookup_fields['fk'])
    fk_fields_list.insert(0, 'template')
    autocomplete_lookup_fields['fk'] = tuple(fk_fields_list)

    m2m_fields_list = list(autocomplete_lookup_fields['m2m'])
    m2m_fields_list.insert(0, 'tags')
    autocomplete_lookup_fields['m2m'] = tuple(m2m_fields_list)

    raw_id_fields = HierarchicalContentAdmin.raw_id_fields
    raw_id_fields_list = list(raw_id_fields)
    raw_id_fields_list.insert(0, 'template')
    raw_id_fields_list.insert(0, 'tags')
    raw_id_fields = tuple(raw_id_fields_list)

    core_fields = HierarchicalContentAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(2, 'template')
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

    fields = ('order','title', 'content_type', 'object_id', 'path', 'target')
    sortable_field_name = 'order'
    extra = 0


class MenuAdmin(BaseVersionableAdmin):

    prepopulated_fields = {"slug": ("title",)}
    core_fields = (
        'title',
        'slug',
    )

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



admin.site.register(Template, TemplateAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageTag, PageTagAdmin)
admin.site.register(Menu, MenuAdmin)