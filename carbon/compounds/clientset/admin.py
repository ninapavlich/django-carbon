from django.contrib import admin

# from .models import *


class ClientSetItemAdminInline(admin.TabularInline):
    # model = ClientSetItem	
    pass

class ClientSetCategoryAdmin(admin.ModelAdmin):
    # inline = [ClientSetItemAdminInline]
    pass

class ClientMediaAdminInline(admin.TabularInline):
    # model = ClientMedia	
    pass

class ClientAdmin(admin.ModelAdmin):
    # inline = [ClientMediaAdminInline]
    pass


# admin.site.register(ClientSetCategory, ClientSetCategoryAdmin)
# admin.site.register(Client, ClientAdmin)