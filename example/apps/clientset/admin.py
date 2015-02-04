from django.contrib import admin

from carbon.compounds.clientset.admin import ClientSetItemAdminInline as BaseClientSetItemAdminInline
from carbon.compounds.clientset.admin import ClientSetCategoryAdmin as BaseClientSetCategoryAdmin
from carbon.compounds.clientset.admin import ClientMediaAdminInline as BaseClientMediaAdminInline
from carbon.compounds.clientset.admin import ClientAdmin as BaseClientAdmin

from .models import *

class ClientSetItemAdminInline(BaseClientSetItemAdminInline):
    model = ClientSetItem	

class ClientSetCategoryAdmin(BaseClientSetCategoryAdmin):
    inline = [ClientSetItemAdminInline]


class ClientMediaAdminInline(BaseClientMediaAdminInline):
    model = ClientMedia	

class ClientAdmin(BaseClientAdmin):
    inline = [ClientMediaAdminInline]


admin.site.register(ClientSetCategory, ClientSetCategoryAdmin)
admin.site.register(Client, ClientAdmin)