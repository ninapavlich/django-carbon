from django.contrib import admin

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
    

class ProjectCategoryAdmin(BaseCategoryAdmin):
    inlines = [ProjectCategoryItemAdminInline]

class ProjectMediaAdminInline(admin.TabularInline):
    model = ProjectMedia    
    extra = 0
    #sortable_field_name = 'order'
    #TODO -- media fields

class ProjectAdmin(BaseContentAdmin):
    inlines = [ProjectMediaAdminInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)