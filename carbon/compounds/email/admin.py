from django.contrib import admin

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from reversion.admin import VersionAdmin
from django_inline_wrestler.admin import TabularInlineOrderable

from carbon.atoms.admin.content import BaseVersionableAdmin, BaseVersionableTitleAdmin

# from .models import *
from .forms import *



class EmailTemplateAdmin(VersionAdmin, BaseVersionableTitleAdmin):
    
    form = EmailTemplateAdminForm
    prepopulated_fields = {"slug": ("title",)}

    core_fields = (
        ('title','slug'),
        'subject_template',
        'body_template',
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Template", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )    

    search_fields = ('title','admin_note', 'subject_template', 'body_template')


class EmailCategoryAdmin(VersionAdmin, BaseVersionableTitleAdmin):

    prepopulated_fields = {"slug": ("title",)}

    autocomplete_lookup_fields = {
        'fk': ('parent',),
        'm2m': ()
    }
    raw_id_fields = ('parent',)

    core_fields = (
        ('edit_parent','parent',),
        ('title','slug'),
        'can_be_viewed_online',
        'requires_explicit_opt_in',
        'can_unsubscribe'
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Category", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    readonly_fields = BaseVersionableAdmin.readonly_fields + ('edit_parent',)
    list_display = ('parent', 'title', 'can_be_viewed_online', 'requires_explicit_opt_in','can_unsubscribe')
    list_display_links = ('parent','title')
list_filter = ('parent','can_be_viewed_online','requires_explicit_opt_in','can_unsubscribe')


class EmailReceiptAdmin(VersionAdmin, BaseVersionableAdmin):

    autocomplete_lookup_fields = {
        'fk': ('category'),
        'm2m': ()
    }
    raw_id_fields = ( 'category',)

    core_fields = (
        ('recipient_email','category'),
        ('rendered_subject'),
        ('rendered_body'),
    )
    stats_fields = (
        ('access_key'),
        ('viewed','view_count'),
        ('first_viewed_date','last_viewed_date')
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Stats", {
            'fields': stats_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    list_display = ('recipient_email','category','rendered_subject','viewed','view_count','first_viewed_date')
    list_filter = ('recipient_email','category','viewed')




class EmailCategorySubscriptionSettingsAdmin(VersionAdmin, BaseVersionableTitleAdmin):

    prepopulated_fields = {"slug": ("title",)}

    autocomplete_lookup_fields = {
        'fk': ('category','parent',),
        'm2m': ()
    }
    raw_id_fields = ('category','parent',)

    core_fields = (
        ('parent','category'),
        'status'
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Category", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )


class EmailCategorySubscriptionSettingsInline(admin.TabularInline):
    #model = EmailCategorySubscriptionSettings  
    fk_name = 'parent'
    autocomplete_lookup_fields = {
        'fk': ('category',),
        'm2m': ()
    }
    raw_id_fields = ('category',)

    fields = ('category','title','status')
    
    extra = 0

class UserSubscriptionSettingsAdmin(VersionAdmin, BaseVersionableAdmin):

    

    core_fields = (
        ('recipient_email',),
        'access_key'
    )
    meta_fields = BaseVersionableAdmin.meta_fields
    fieldsets = (
        ("Category", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    list_display = ('recipient_email',)
    list_filter = ('recipient_email',)

    # inlines = [EmailCategorySubscriptionSettingsInline]




# admin.site.register(EmailTemplate, EmailTemplateAdmin)
# admin.site.register(EmailCategory, EmailCategoryAdmin)
# admin.site.register(EmailReceipt, EmailReceiptAdmin)
# admin.site.register(EmailCategorySubscriptionSettings, EmailCategorySubscriptionSettingsAdmin)
# admin.site.register(UserSubscriptionSettings, UserSubscriptionSettingsAdmin)