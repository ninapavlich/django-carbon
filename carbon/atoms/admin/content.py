from django.contrib import admin

from carbon.atoms.models.content import PublishableAtom




class BaseVersionableAdmin(admin.ModelAdmin):

    class Media:        
        css = {
            "all": ('admin/css/adjustments.css',)
        }

    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
    )   

    
    meta_fields = (
        ('version'),
        ('created_date', 'created_by'),
        ('modified_date', 'modified_by'),
        'admin_note'
    )

    fieldsets = (
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    list_filter = (
            "created_by", "modified_by", )

    def save_model(self, request, obj, form, change):
        if not getattr(obj, "created_by"):
            obj.created_by = request.user
        obj.modified_by = request.user


        super(BaseVersionableAdmin, self). save_model(request, obj, form, change)



class BaseVersionableTitleAdmin(BaseVersionableAdmin):

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


class BaseContentAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/adjustments.css',)
        }
        js = ('animations.js', 'actions.js')

    def admin_hierarchy(self, obj):
        return obj.admin_hierarchy
    admin_hierarchy.allow_tags = True
    
    autocomplete_lookup_fields = {
        'fk': ('image', 'published_by', 'template'),
        'm2m': ()
    }
    raw_id_fields = ( 'image', 'published_by', 'template')
    
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
        ('publication_status'),
        ('template', 'edit_template'),
        'content',
        'synopsis',
        ('image_preview','image')
    )

    publication_fields = (
        ('publication_date', 'published_by'),
        ('publish_on_date', 'expire_on_date'),
        'facebook_author_id',
        'twitter_author_id',
        'google_author_id'
    )
   
    path_fields = (
        ('path', 'uuid'),
        ('path_generated', 'path_override'),
        ('temporary_redirect', 'permanent_redirect'),
        'order'

    )

    seo_fields = (
        'page_meta_description',
        'page_meta_keywords',
        ('is_searchable','in_sitemap'),
        ('sitemap_changefreq','sitemap_priority'),
        ('noindex','nofollow')
    )

    social_fields = (
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
            'classes': ( 'grp-collapse', )
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

    def save_model(self, request, obj, form, change):
       

        if obj.pk is not None and obj.publication_status == PublishableAtom.PUBLISHED:
            original = type(obj).objects.get(pk=obj.pk)
            if original.publication_status != obj.publication_status:
                if not obj.published_by:
                    obj.published_by = request.user

        super(BaseContentAdmin, self). save_model(request, obj, form, change)


class HierarchicalContentAdmin(BaseContentAdmin):
    

    
    autocomplete_lookup_fields = BaseContentAdmin.autocomplete_lookup_fields
    fk_fields_list = list(autocomplete_lookup_fields['fk'])
    fk_fields_list.insert(0, 'parent')
    autocomplete_lookup_fields['fk'] = tuple(fk_fields_list)


    raw_id_fields = BaseContentAdmin.raw_id_fields
    raw_id_fields_list = list(raw_id_fields)
    raw_id_fields_list.insert(0, 'parent')
    raw_id_fields = tuple(raw_id_fields_list)


    core_fields = BaseContentAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(0, ('edit_parent','parent'))
    core_fields = tuple(core_fields_list)

    list_filter = BaseContentAdmin.list_filter
    list_filter_list = list(list_filter)
    list_filter_list.insert(0, 'parent')
    list_filter = tuple(list_filter_list)

    path_fields = BaseContentAdmin.path_fields
    publication_fields = BaseContentAdmin.publication_fields
    seo_fields = BaseContentAdmin.seo_fields
    social_fields = BaseContentAdmin.social_fields
    meta_fields = BaseVersionableAdmin.meta_fields

    readonly_fields = BaseContentAdmin.readonly_fields + ('edit_parent',)

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

