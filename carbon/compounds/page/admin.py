from django.contrib import admin

from carbon.atoms.admin.content import HierarchicalContentAdmin

from .models import *



class TemplateAdmin(admin.ModelAdmin):
    pass


class PageAdmin(HierarchicalContentAdmin):
    pass

class PageCategoryItemAdminInline(admin.TabularInline):
    model = PageCategoryItem    

class PageCategoryAdmin(admin.ModelAdmin):
    inline = [PageCategoryItemAdminInline]


admin.site.register(Template, TemplateAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageCategory, PageCategoryAdmin)