from django.contrib import admin

from carbon.compounds.portfolio.admin import ProjectCategoryItemAdminInline as BaseProjectCategoryItemAdminInline
from carbon.compounds.portfolio.admin import ProjectCategoryItemInProjectAdminInline as BaseProjectCategoryItemInProjectAdminInline
from carbon.compounds.portfolio.admin import ProjectCategoryAdmin as BaseProjectCategoryAdmin
from carbon.compounds.portfolio.admin import ProjectAdmin as BaseProjectAdmin

from .models import *

class ProjectCategoryItemAdminInline(BaseProjectCategoryItemAdminInline):

    model = ProjectCategoryItem    

class ProjectCategoryItemInProjectAdminInline(BaseProjectCategoryItemInProjectAdminInline):
    
    model = ProjectCategoryItem
    
    

class ProjectCategoryAdmin(BaseCategoryAdmin):
    inlines = [ProjectCategoryItemAdminInline]

class ProjectMediaAdminInline(BaseProjectCategoryAdmin):
    model = ProjectMedia    
    

class ProjectAdmin(BaseProjectAdmin):
    inlines = [ProjectMediaAdminInline, ProjectCategoryItemInProjectAdminInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)