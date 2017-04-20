from django.contrib import admin
from django.utils.safestring import mark_safe

from .content import *

class BaseTagAdmin(BaseContentAdmin):

    def admin_hierarchy(self, obj):
        return mark_safe(obj.admin_hierarchy)

    autocomplete_lookup_fields = {
        'fk': ('template','image'),
    }
    raw_id_fields = ( 'template','image')
    
    
    list_display = ( "admin_hierarchy", "path",  "title", "publication_status",)
    list_display_links = ( "admin_hierarchy", "path", "title",)
    list_filter = (
            "publication_status", "created_by", "modified_by", 
            'published_by','is_searchable','in_sitemap',
            'sitemap_changefreq','sitemap_priority','noindex','nofollow',
            'shareable','social_share_type')
    ordering = ("hierarchy",)



    prepopulated_fields = {"slug": ("title",)}
    
    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
         "path", "path_generated", "uuid", 'image_preview', 'edit_template'
    )
    


    core_fields = (
        ('title','slug'),
        'content',
        'synopsis',
        ('image_preview','image')

    )

    publication_fields = (
        ('publication_status'),
        ('publication_date', 'published_by'),
        ('publish_on_date', 'expire_on_date'),
        'facebook_author_id',
        'twitter_author_id',
        'google_author_id'
    )
   
    path_fields = (
        ('template', 'edit_template'),
        ('path', 'uuid',),
        ('path_generated', 'path_override'),
        ('temporary_redirect', 'permanent_redirect'),
        'order'

    )

    seo_fields = BaseContentAdmin.seo_fields
    social_fields =  (
        ('shareable','social_share_type'),
        'tiny_url',
        'social_share_image',        
    )
    meta_fields = BaseVersionableAdmin.meta_fields


    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Path", {
            'fields': path_fields,
            'classes': ( 'grp-collapse grp-open', )
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

class BaseSimplifiedTagAdmin(BaseContentAdmin):

    def admin_hierarchy(self, obj):
        return mark_safe(obj.admin_hierarchy)
    

    list_display = ( "admin_hierarchy", "path",  "title", "publication_status",)
    list_display_links = ( "admin_hierarchy", "path", "title",)
    list_filter = (
        "publication_status", "created_by", "modified_by", 
    )
    ordering = ("hierarchy",)



    prepopulated_fields = {"slug": ("title",)}
    
    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
    )
    
    


    core_fields = (
        ('title','slug'),
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

class BaseCategoryAdmin(BaseTagAdmin):

    autocomplete_lookup_fields = {
        'fk': ('parent','template','image'),
    }
    raw_id_fields = ( 'parent','template','image')

    core_fields = BaseTagAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(0, ('edit_parent','parent'))
    core_fields = tuple(core_fields_list)

    list_filter = BaseTagAdmin.list_filter
    list_filter_list = list(list_filter)
    list_filter_list.insert(0, 'parent')
    list_filter = tuple(list_filter_list)

    path_fields = BaseTagAdmin.path_fields
    publication_fields = BaseTagAdmin.publication_fields
    seo_fields = BaseTagAdmin.seo_fields
    social_fields = BaseTagAdmin.social_fields
    meta_fields = BaseTagAdmin.meta_fields

    readonly_fields = BaseTagAdmin.readonly_fields + ('edit_parent',)

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

class BaseSimplifiedCategoryAdmin(BaseSimplifiedTagAdmin):

    autocomplete_lookup_fields = {
        'fk': ('parent',),
    }
    raw_id_fields = ( 'parent',)

    core_fields = BaseSimplifiedTagAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(0, ('edit_parent','parent'))
    core_fields = tuple(core_fields_list)

    list_filter = BaseSimplifiedTagAdmin.list_filter
    list_filter_list = list(list_filter)
    list_filter_list.insert(0, 'parent')
    list_filter = tuple(list_filter_list)

    
    meta_fields = BaseSimplifiedTagAdmin.meta_fields

    readonly_fields = BaseSimplifiedTagAdmin.readonly_fields + ('edit_parent',)

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