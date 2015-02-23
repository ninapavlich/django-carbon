from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from .models import *
from .forms import *



class BlogArticleRoleInline(admin.TabularInline):
    #model = BlogArticleRole
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }
    raw_id_fields = ('user',)

    fields = ('order', 'user', 'role')
    

    sortable_field_name = 'order'
    extra = 0


class BlogArticleAdmin(BaseContentAdmin):
    form = BlogArticleAdminForm

    autocomplete_lookup_fields = {
        'fk': ('image', 'published_by', 'template', 'category'),
        'm2m': ('tags','related')
    }
    raw_id_fields = ( 'image', 'published_by', 'template','category', 'tags', 
        'related')
    

    core_fields = BaseContentAdmin.core_fields
    core_fields_list = list(core_fields)
    core_fields_list.insert(5, 'category')
    core_fields_list.insert(5, 'related')
    core_fields_list.insert(5, 'tags')    
    core_fields = tuple(core_fields_list)

    path_fields = BaseContentAdmin.path_fields
    publication_fields = BaseContentAdmin.publication_fields
    seo_fields = BaseContentAdmin.seo_fields
    
    social_fields = BaseContentAdmin.social_fields
    social_fields_list = list(social_fields)
    social_fields_list.insert(1, 'allow_comments')
    social_fields = tuple(social_fields_list)
    

    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Roles", {
            'fields': (),
            'classes': ( 'placeholder blogarticlerole_set-group', )
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

class BlogTagAdmin(BaseTagAdmin):
    pass

class BlogCategoryAdmin(BaseCategoryAdmin):
    pass    


# admin.site.register(BlogArticle, BlogArticleAdmin)
# admin.site.register(BlogTag, BlogTagAdmin)
# admin.site.register(BlogCategory, BlogCategoryAdmin)