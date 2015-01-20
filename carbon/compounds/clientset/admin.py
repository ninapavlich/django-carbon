from django.contrib import admin

from .models import *


class ClientSetItemAdminInline(admin.TabularInline):
    model = ClientSetItem	

class ClientSetCategoryAdmin(admin.ModelAdmin):
    inline = [ClientSetItemAdminInline]


class ClientMediaAdminInline(admin.TabularInline):
    model = ClientMedia	

class ClientAdmin(admin.ModelAdmin):
    inline = [ClientMediaAdminInline]


admin.site.register(ClientSetCategory, ClientSetCategoryAdmin)
admin.site.register(Client, ClientAdmin)