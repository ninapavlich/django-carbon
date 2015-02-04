from django.contrib import admin

from carbon.compounds.core.admin import TemplateAdmin as BaseTemplateAdmin

from .models import *

class TemplateAdmin(BaseTemplateAdmin):
    pass

admin.site.register(Template, TemplateAdmin)