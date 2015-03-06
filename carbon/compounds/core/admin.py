from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from reversion.admin import VersionAdmin

# from .models import *
from .forms import *


class TemplateAdmin(VersionAdmin, BaseTemplateAdmin):
    form = TemplateAdminForm

# admin.site.register(Template, TemplateAdmin)