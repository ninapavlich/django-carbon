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
    #model = MenuItem
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': [],
    }


    fields = ('order', 'title',  'content_type', 'object_id', 'path_override', 'target', 'publication_status', 'publish_on_date', 'expire_on_date')
    

    sortable_field_name = 'order'
    extra = 0


class MenuItemAdmin(BaseVersionableAdmin):

    
    core_fields = (
        ('title','slug'),
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
    readonly_fields = BaseVersionableAdmin.readonly_fields + ('path',)
    # inlines = [MenuItemInline]


class LegacyURLRefererInline(admin.TabularInline):
    #model = LegacyURLReferer

    fields = ('referer_title','referer_url', 'created_date')
    extra = 0

    readonly_fields = BaseVersionableAdmin.readonly_fields


class LegacyURLAdmin(BaseVersionableAdmin):

    def visit_old_link(self, obj):
        return "<a href='%s%s' target='_blank'>Visit Old Link</a>"%(settings.LEGACY_URL_ARCHIVE_DOMAIN, obj.url)
    visit_old_link.allow_tags = True


    def test_redirect(self, obj):
        return "<a href='%s' target='_blank'>Test Redirect</a>"%(obj.url)
    test_redirect.allow_tags = True

    
    core_fields = (
        ('url'),
        ( 'content_type', 'object_id',),
        ('path_override'),
        ('path'),
        ('visit_old_link','test_redirect')
    )
    

    list_display = ( "url", "path",'created_date')
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



# admin.site.register(Page, PageAdmin)
# admin.site.register(PageTag, PageTagAdmin)
# admin.site.register(MenuItem, MenuItemAdmin)