from django.contrib import admin
from django.core.urlresolvers import reverse

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from reversion.admin import VersionAdmin

from .models import *
# from .forms import *

from django_inline_wrestler.admin import TabularInlineOrderable

class FormFieldInline(admin.StackedInline):
    #model = FormField
    # form = FormFieldInlineAdminForm
  
    ordering = ("order",)
    sortable_field_name = 'order'
    core_fields = (
        ('type','order'),
        ('title', 'slug'),
        ('secondary_label','placeholder_text',),
        ('help_text','default'),
    )

    advanced_properties = (
        'hide',
        'choices',
        'extra_css_classes',
        ('icon_left', 'icon_right'),
        ('inset_text_left', 'inset_text_right'),
        'content',
    )
    validation_options = (
        'is_required',
        ('is_email','is_url'),
        ('is_number','is_integer'),
        ('is_digits','is_alphanumeric'),
        ('min_length','max_length'),
        ('step_interval'),
        ('min_value','max_value'),
        ('min_words','max_words'),
        ('min_check','max_check'),
        ('min_date','max_date'),
        ('min_time', 'max_time'),
        # ('min_characters','max_characters'),        
        'equal_to',
        'pattern'
    )


    fieldsets = (
        ("Basic Properties", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Advanced Properties", {
            'fields': advanced_properties,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Validation Options", {
            'fields': validation_options,
            'classes': ( 'grp-collapse grp-closed', )
        }),
    ) 
    classes = ('grp-collapse grp-open',)
    readonly_fields = ('slug',)
    # prepopulated_fields = {"slug": ("title",)}
    extra = 0  
    

class FormAdmin(VersionAdmin, BaseContentAdmin):
    core_fields = (
        ('title','slug'),
        ('publication_status'),
        ('template', 'submit_template'),
        ('form_action',),
        ('required_logged_in_user','is_editable'),
        ('email_admin_on_submission', 'email_user_on_submission'),
        ('redirect_url_on_submission',),
        ('submit_label', 'extra_css_classes'),
        ('submission_content')
    )

    additional_fields = (
        'content',
        'synopsis',
        ('image_preview','image')
    )

    autocomplete_lookup_fields = {
        'fk': ('image', 'published_by', 'template', 'submit_template'),
        'm2m': ()
    }
    raw_id_fields = ( 'image', 'published_by', 'template', 'submit_template')

    publication_fields = BaseContentAdmin.publication_fields
   
    path_fields = BaseContentAdmin.path_fields

    seo_fields = BaseContentAdmin.seo_fields

    social_fields = BaseContentAdmin.social_fields
    
    meta_fields = BaseVersionableAdmin.meta_fields
    


    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Additional Content", {
            'fields': additional_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Path", {
            'fields': path_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Publication", {
            'fields': publication_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        
        ("Search Engine Optimization", {
            'fields': seo_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Social Integration", {
            'fields': social_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )


class FormEntryAdmin(VersionAdmin, BaseVersionableAdmin):
    
    list_display = ( "form_schema", "pk", "created_date",  "created_by", "admin_note",)


    autocomplete_lookup_fields = {
        'fk': ('form_schema'),
    }
    raw_id_fields = ( 'form_schema',)

    core_fields = (
        ('form_schema'),
    )
    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Form", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )


class FieldEntryAdmin(VersionAdmin, BaseVersionableAdmin):

    autocomplete_lookup_fields = {
        'fk': ('form_entry', 'form_field'),
    }
    raw_id_fields = ('form_entry', 'form_field',)

    core_fields = (
        'form_field',
        ('form_entry',),
        ('value')
    )
    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Form", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

class FieldEntryInline(TabularInlineOrderable):
    #model = FieldEntry    

    readonly_fields = ('form_field',)
    autocomplete_lookup_fields = {
        'fk': ('form_entry', 'form_field',),
    }
    raw_id_fields = ('form_entry', 'form_field',)

    fields = ('form_field', 'value')
    extra = 0
