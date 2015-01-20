from django.contrib import admin

from carbon.atoms.admin.content import *

from .models import *



class TemplateAdmin(BaseVersionableAdmin):

    core_fields = (
        'title',
        'content',
    )

    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': BaseVersionableAdmin.meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )



class PageAdmin(HierarchicalContentAdmin):

    autocomplete_lookup_fields = HierarchicalContentAdmin.autocomplete_lookup_fields
    fk_fields_list = list(autocomplete_lookup_fields['fk'])
    fk_fields_list.insert(0, 'template')
    autocomplete_lookup_fields['fk'] = tuple(fk_fields_list)


    raw_id_fields = HierarchicalContentAdmin.raw_id_fields
    raw_id_fields_list = list(raw_id_fields)
    raw_id_fields_list.insert(0, 'template')
    raw_id_fields = tuple(raw_id_fields_list)

    core_fields = HierarchicalContentAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(2, 'template')
    core_fields = tuple(core_fields_list)

    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Path", {
            'fields': BaseContentAdmin.path_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Publication", {
            'fields': BaseContentAdmin.publication_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Search Engine Optimization", {
            'fields': BaseContentAdmin.seo_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Social Integration", {
            'fields': BaseContentAdmin.social_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Meta", {
            'fields': BaseVersionableAdmin.meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )


class PageCategoryItemAdminInline(admin.TabularInline):
    model = PageCategoryItem    
    extra = 0

    fields = ('order','item')

    autocomplete_lookup_fields = {
        'fk': ('item',),
    }
    raw_id_fields = ( 'item',)
    sortable_field_name = 'order'

class PageCategoryAdmin(BaseCategoryAdmin):
    inlines = [PageCategoryItemAdminInline]


admin.site.register(Template, TemplateAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageCategory, PageCategoryAdmin)