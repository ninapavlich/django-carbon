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
        'content',
        'extra_css_classes',
        ('icon', 'prefix')        
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
    pass