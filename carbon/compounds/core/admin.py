from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

# from .models import *
from .forms import *


class TemplateAdmin(BaseTemplateAdmin):
    form = TemplateAdminForm

# admin.site.register(Template, TemplateAdmin)