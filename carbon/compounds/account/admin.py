from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as ContribUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import *
# from .models import User, Organization





class UserAdmin(ContribUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    add_fieldsets = (
        ("User", {
            'classes': (),
            'fields': ('email', 'password1', 'password2','first_name','last_name',)}
        ),
    )

    fieldsets = (
        ('Name', { 
            'fields': (
                ("first_name","last_name"),
                ('email','date_of_birth'),
                'password',
            )
        }),
        (_('CMS Permissions'), {
            'fields': (
                ('is_active', 'is_staff',),
                
                'is_superuser',
                ('groups')
            )
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    
    #readonly_fields = ('last_login','date_joined', 'impersonate_user')



class OrganizationAdmin(admin.ModelAdmin):
    pass
    


# admin.site.register(Organization, OrganizationAdmin)    
# admin.site.register(User, UserAdmin)


