from django.contrib import admin
from django.core.urlresolvers import reverse

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from .models import *


class ProjectCategoryItemAdminInline(admin.TabularInline):
    model = ProjectCategoryItem
    extra = 0
    sortable_field_name = 'order'

    fields = ('order','item')

    autocomplete_lookup_fields = {
        'fk': ('item',),
    }
    raw_id_fields = ( 'item',)

class ProjectCategoryItemInProjectAdminInline(admin.TabularInline):
    def edit_url(self, obj):
        if obj.category:
            object_type = type(obj.category).__name__            
            url = reverse('admin:%s_%s_change' %(obj.category._meta.app_label,  obj.category._meta.module_name),  args=[obj.category.id] )
            return u"<a href='%s' >Edit Category</a>"%(url)
        
    edit_url.allow_tags = True

    model = ProjectCategoryItem
    extra = 0
    
    fields = ('category','edit_url')

    autocomplete_lookup_fields = {
        'fk': ('category',),
    }
    raw_id_fields = ( 'category',) 
    readonly_fields = ('edit_url',)   
    

class ProjectCategoryAdmin(BaseCategoryAdmin):
    inlines = [ProjectCategoryItemAdminInline]

class ProjectMediaAdminInline(admin.TabularInline):
    model = ProjectMedia    
    extra = 0
    sortable_field_name = 'order'
    
    def preview(self, obj):
        if obj.image:
            try:
                return "<img src='%s' alt='%s preview'/>"%(obj.image.thumbnail.url, obj.title)
            except:
                return ""
        return ''
    preview.allow_tags = True

    fields = (
        'order',
        'preview',
        'title',
        'file',
        'image',
        ('clean_filename_on_upload','allow_overwrite'),
        ('alt',),
        'credit',
        'caption',

    )
    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "preview",
    )

class ProjectAdmin(BaseContentAdmin):
    inlines = [ProjectMediaAdminInline, ProjectCategoryItemInProjectAdminInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)