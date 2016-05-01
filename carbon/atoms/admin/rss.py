from django.contrib import admin

from carbon.atoms.admin.content import BaseVersionableAdmin, BaseVersionableTitleAdmin



class BaseRSSUrlAdmin(BaseVersionableTitleAdmin):

    
    def sync_rss(modeladmin, request, queryset):
        for item in queryset:
            item.sync_rss()
    sync_rss.short_description = "Sync RSS"


    core_fields = (
        ('title','slug'),
        'url',
        'last_imported',
        'active',
        'logo_url',
        ('logo_width','logo_height'),
        'regex'
    )
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        
        ("Meta", {
            'fields': BaseVersionableTitleAdmin.meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    list_display = ['title', 'url', 'last_imported', 'active']
    actions = [sync_rss]
