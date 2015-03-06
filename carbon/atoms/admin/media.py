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

    def image_variants(self, obj):

        if obj.image:
            base_image =  '<a href="%s" target="_blank">Original Size (%spx x %spx)</a><br />'%(obj.image_url, obj.image_width, obj.image_height)
            for variant in obj.__class__.variants:
                image_variant_name = variant.replace("_", " ").title()
                base_image +=  '<a href="%s" target="_blank">%s (%spx x %spx)</a><br />'%(obj.get_variant_url(variant), image_variant_name, obj.get_variant_width(variant), obj.get_variant_height(variant))

            return base_image
    image_variants.allow_tags = True


    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "preview", "image_variants"
    )
    
    core_fields = (
        'title',
        ('image','preview'),
        ('image_variants'),
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
