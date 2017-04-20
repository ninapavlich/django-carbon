from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as ContribUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import *
# from .models import User, Organization

from reversion.admin import VersionAdmin
from django_inline_wrestler.admin import TabularInlineOrderable

from carbon.atoms.admin.content import BaseVersionableAdmin, BaseVersionableTitleAdmin



class UserAdmin(ContribUserAdmin):
    def preview(self, obj):
        if obj.image:
            try:
                return mark_safe("<img src='%s' alt='%s preview'/>"%(obj.image.thumbnail_url, obj.image.title))
            except:
                return ""
        return ''
    

    autocomplete_lookup_fields = {
        'fk': ['image',],
    }
    raw_id_fields = ('image',)

    form = UserChangeForm
    add_form = UserCreationForm
    add_fieldsets = (
        ("User", {
            'classes': (),
            'fields': ('email', 'password1', 'password2','first_name','last_name',)}
        ),
    )

    fieldsets = (
        ('User', { 
            'fields': (
                ("first_name","last_name"),
                ('email','date_of_birth'),
                'password',
                'about',
                ('preview','image')
            ),
            'classes': ( 'grp-collapse grp-open', )
        }),
        (_('CMS Permissions'), {
            'fields': (
                ('is_active', 'is_staff',),
                
                'is_superuser',
                ('groups')
            ),
            'classes': ( 'grp-collapse grp-closed', )
        }),
    )

    list_display = ('preview','email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_display_links = ('preview','email','first_name','last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ContribUserAdmin.readonly_fields + ('preview',)
    #'last_login','date_joined', 'impersonate_user'




class UserGroupAdmin(VersionAdmin, BaseVersionableTitleAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

    form = UserGroupAdminForm

    core_fields = (
        ('title','slug'),
        ('synopsis'),
        ('content')
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    search_fields = ('title','admin_note', 'synopsis', 'content')


class UserGroupMemberInGroupAdmin(TabularInlineOrderable):
    #model = UserGroupMember

    def edit_member_link(self, obj):
        if obj.user:
            try:
                return mark_safe("<a href='%s'>Edit User></a>"%(obj.user.edit_item_url))
            except:
                return ""
        return ''

    fk_name = 'group'
    autocomplete_lookup_fields = {
        'fk': ['user',],
    }
    raw_id_fields = ('user',)
    fields = ('order','user','edit_member_link')
    extra = 0
    readonly_fields = ('edit_member_link',)

class UserGroupMemberInUserAdmin(admin.TabularInline):
    #model = UserGroupMember

    def all_members_link(self, obj):
        if obj.group:
            try:
                return mark_safe("<a href='%s'>See All Members ></a>"%(obj.group.edit_item_url))
            except:
                return ""
        return ''

    fk_name = 'user'
    autocomplete_lookup_fields = {
        'fk': ['group',],
    }
    raw_id_fields = ('group',)
    fields = ('group','all_members_link',)
    extra = 0    
    readonly_fields = ('all_members_link',)


class OrganizationAdmin(VersionAdmin, BaseVersionableTitleAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

    core_fields = (
        ('title','slug'),
        ('synopsis'),
        ('content')
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    search_fields = ('title','admin_note', 'synopsis', 'content')
    
    

class SocialContactLinkInline(TabularInlineOrderable):
    # model = SocialContactLink
    fk_name = 'user'    
    fields = ('order','title','url','icon', 'css_classes', 'extra_attributes')
    extra = 0

# admin.site.register(Organization, OrganizationAdmin)    
# admin.site.register(User, UserAdmin)


