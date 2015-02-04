from django.contrib import admin

from carbon.compounds.account.admin import UserAdmin as BaseUserAdmin
from carbon.compounds.account.admin import OrganizationAdmin as BaseOrganizationAdmin

from .models import *

class UserAdmin(BaseUserAdmin):
    pass



class OrganizationAdmin(BaseOrganizationAdmin):
    pass
    

admin.site.register(Organization, OrganizationAdmin)    
admin.site.register(User, UserAdmin)