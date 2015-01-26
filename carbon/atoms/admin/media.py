from django.contrib import admin

from .content import *

class BaseImageAdmin(BaseVersionableAdmin):

    def preview(self, obj):
        if obj.image:
            try:
                return "<img src='%s' alt='%s preview'/>"%(obj.thumbnail.url, obj.title)
            except:
                return ""
        return ''
    preview.allow_tags = True


    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        'preview'
    )
    
    core_fields = (
        'title',
        ('image','preview'),
        ('clean_filename_on_upload','allow_overwrite'),
        ('alt','use_png'),
        'credit',
        'caption',

    )

    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Image", {
            'fields': core_fields,
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    list_display = ('title','preview',)

class BaseMediaAdmin(BaseVersionableAdmin):

    autocomplete_lookup_fields = {
        'fk': ('image', ),
    }
    raw_id_fields = ( 'image', )

    readonly_fields = BaseVersionableAdmin.readonly_fields
    
    core_fields = (
        'title',
        ('file','image'),
        ('clean_filename_on_upload','allow_overwrite'),
        'credit',
        'caption',

    )

    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Image", {
            'fields': core_fields,
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
