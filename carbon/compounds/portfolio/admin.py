from django.contrib import admin

from carbon.atoms.admin.content import BaseContentAdmin

from .models import *


class ProjectCategoryItemAdminInline(admin.TabularInline):
	model = ProjectCategoryItem

class ProjectCategoryAdmin(admin.ModelAdmin):
	inline = [ProjectCategoryItemAdminInline]

class ProjectMediaAdminInline(admin.TabularInline):
    model = ProjectMedia	

class ProjectAdmin(BaseContentAdmin):
    inline = [ProjectMediaAdminInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)