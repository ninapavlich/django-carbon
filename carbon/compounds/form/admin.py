from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from carbon.atoms.admin.content import *
from carbon.atoms.admin.taxonomy import *

from reversion.admin import VersionAdmin

from .models import *
# from .forms import *

from django_inline_wrestler.admin import TabularInlineOrderable


class FormEntryStatusAdmin(BaseTagAdmin):
    pass

class FormEntryTagAdmin(BaseTagAdmin):
    pass

class FormFieldInline(admin.StackedInline):
    #model = FormField
    # form = FormFieldInlineAdminForm
  
    ordering = ("order",)
    sortable_field_name = 'order'
    core_fields = (
        ('type','order'),
        ('title', 'slug'),
        ('secondary_label','help_text',),
        ('placeholder_text','default'),
        ('is_required', 'hide',),
        'error_message',
        'choices',
    )

    additional_content = (              
        'extra_css_classes',
        'third_party_id',
        # ('icon_left', 'icon_right'),
        # ('inset_text_left', 'inset_text_right'),
        'content',
    )
    validation_options = (
        ('is_digits','is_alphanumeric'),
        ('min_length','max_length'),
        # ('step_interval'),
        ('min_value','max_value'),
        ('min_words','max_words'),
        

        ('min_width', 'max_width'),
        ('min_height', 'max_height'),
        ('min_size', 'max_size'),

        # ('min_check','max_check'),
        ('min_date','min_datetime'),
        ('max_date', 'max_datetime'),
        
        
        ('equal_to', 'equal_to_error_message'),
        ('pattern', 'pattern_error_message')
    )


    fieldsets = (
        ("Basic Properties", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Additional Content", {
            'fields': additional_content,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Advanced Validation Options", {
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
    )
    form_behavior = (
        'redirect_url_on_submission',
        'form_action',
        'required_logged_in_user',
        'is_editable',      
        
        'extra_css_classes',
        'third_party_id'
    )
    form_messages_and_abels = (
        'submit_label',
        'form_create_message',
        'form_update_message',
        'form_error_message',
    )
    email_email_fields = (
        'email_admin_on_submission',
        'email_admin_override',
        'email_admin_on_submission_category',
        'email_admin_on_submission_template',
    
        'email_user_on_submission',
        'email_user_field_slug',
        'email_user_on_submission_template',
        'email_user_on_submission_category'
    )
    

    additional_content_fields = (
        ('publication_status'),
        ('image_preview','image'),
        'template',
        'synopsis',
        'content',
        ('submit_template'),
        ('submission_content'),
    )

    autocomplete_lookup_fields = {
        'fk': ('image', 'published_by', 'template', 'submit_template', 
            'email_admin_on_submission_template', 'email_user_on_submission_template',
            'email_admin_on_submission_category', 'email_user_on_submission_category'),
        'm2m': ()
    }
    raw_id_fields = ( 'image', 'published_by', 'template', 'submit_template', 
        'email_admin_on_submission_template', 'email_user_on_submission_template',
        'email_admin_on_submission_category', 'email_user_on_submission_category')

    publication_fields = BaseContentAdmin.publication_fields
   
    path_fields = BaseContentAdmin.path_fields

    seo_fields = BaseContentAdmin.seo_fields

    social_fields = BaseContentAdmin.social_fields
    
    meta_fields = BaseVersionableAdmin.meta_fields
    


    fieldsets = (
        ("Form Title", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Form Behavior", {
            'fields': form_behavior,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Form Messages & Labels", {
            'fields': form_messages_and_abels,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Form Email Behavior", {
            'fields': email_email_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Additional Content  (For Standalone Forms only)", {
            'fields': additional_content_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Path (For Standalone Forms only)", {
            'fields': path_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Publication (For Standalone Forms only)", {
            'fields': publication_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        
        ("Search Engine Optimization (For Standalone Forms only)", {
            'fields': seo_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Social Integration (For Standalone Forms only)", {
            'fields': social_fields,
            'classes': ( 'grp-collapse grp-closed', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )


class FormEntryAdmin(VersionAdmin, BaseVersionableAdmin):

    def mark_new(modeladmin, request, queryset):
        queryset.update(status=FormEntry.NEW)
    mark_new.short_description = "Mark selected entries as new"

    def mark_read(modeladmin, request, queryset):
        queryset.update(status=FormEntry.READ)
    mark_read.short_description = "Mark selected entries as read"

    def mark_replied(modeladmin, request, queryset):
        queryset.update(status=FormEntry.REPLIED)
    mark_replied.short_description = "Mark selected entries as replied"

    def mark_archived(modeladmin, request, queryset):
        queryset.update(status=FormEntry.ARCHIVED)
    mark_archived.short_description = "Archive selected entries"
    
    actions = [mark_new, mark_read, mark_replied, mark_archived]

    list_display = ( "form_schema", "pk", "created_date",  "admin_note",'status',)
    list_filter = ("form_schema", "created_date", 'status', 'tags', "created_by", "modified_by",)

    autocomplete_lookup_fields = {
        'fk': ('form_schema',),
        'm2m': ('tags',)
    }
    raw_id_fields = ( 'form_schema','tags')

    core_fields = (
        ('form_schema'),
        ('status'),
        ('tags')
    )
    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Form", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-open', )
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



class FieldEntryInline(admin.TabularInline):
    #model = FieldEntry    

    def rendered_value(self, obj):
        return mark_safe(obj.get_rendered_value())

    


    readonly_fields = ('form_field', 'rendered_value')
    fields = ('form_field', 'value', 'rendered_value')
    extra = 0
