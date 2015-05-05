from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.abstract import *
from carbon.atoms.models.content import *

class Form(VersionableAtom, AddressibleAtom, PublishableAtom, SEOAtom):
    help = {
        'form_action': "Current publication status",
        'admin_email':"",
        'email_admin_on_submission':"",
        'email_admin_on_submission_template':"",
        'email_user_on_submission_template':"",
        'submission_content':"",
        'redirect_url_on_submission':""
    }

    POST_TO_FORM_PAGE = 'form-page'
    POST_TO_EMBEDDED_PAGE = 'embedded-page'
    FORM_ACTION_CHOICES = (
        (POST_TO_FORM_PAGE, _("Form Page")),
        (POST_TO_EMBEDDED_PAGE, _("Embedded Page"))
    )

    form_action = models.CharField(max_length=255, choices=FORM_ACTION_CHOICES, 
        default=POST_TO_FORM_PAGE, help_text=help['form_action'])


    email_admin_on_submission = models.BooleanField(default=True, 
        help_text=help['email_admin_on_submission'])
    # email_admin_on_submission_template = models.ForeignKey(settings.EMAIL_TEMPLATE_MODEL, 
    #     null=True, blank=True, help_text=help['email_admin_on_submission_template'])
    admin_email = models.EmailField(max_length=255, blank=False, unique=True,
        help_text=help['admin_email'])

    email_user_on_submission = models.BooleanField(default=True, 
        help_text=help['email_admin_on_submission'])
    # email_user_on_submission_template = models.ForeignKey(settings.EMAIL_TEMPLATE_MODEL, 
    #     null=True, blank=True, help_text=help['email_user_on_submission_template'])

    redirect_url_on_submission = models.CharField(max_length=255, null=True, 
        blank=True, help_text=help['redirect_url_on_submission'])

    submission_content = models.TextField(help_text=help['submission_content'], 
        null=True, blank=True)

    class Meta:
        abstract = True


class FormField(VersionableAtom, TitleAtom):

    help = {
        'order': "",
        'type':"",
        'secondary_label':"",
        'placeholder_text':"",
        'help_text':"",
        'content':"",
        'default':"",
        'choices':"Comma separated options where applicable. If an option "
            "itself contains commas, surround the option starting with the %s"
            "character and ending with the %s character." %
                (settings.FORM_CHOICES_QUOTE, settings.FORM_CHOICES_UNQUOTE)
    }


    TEXT_FIELD = 'text-field'
    TEXT_AREA = 'text-area'
    BOOLEAN_CHECKBOXES = 'boolean-checkboxes'
    BOOLEAN_BUTTONS = 'boolean-buttons'
    SELECT_DROPDOWN = 'select-dropdown'
    SELECT_RADIO_BUTTONS = 'select-radio-buttons'
    SELECT_BUTTONS = 'select-buttons'
    SELECT_MULTIPLE_CHECKBOXES = 'select-multiple-checkboxes'
    SELECT_MULTIPLE_AUTOSUGGEST = 'select-multiple-autosuggest'
    SELECT_MULTIPLE_HORIZONTAL = 'select-multiple-horizontal'
    FORM_INSTRUCTIONS = 'form-instructions'
    FORM_DIVIDER = 'form-divider'
    FORM_STEP = 'form-step'
        
    FORM_FIELD_CHOICES = (
        (TEXT_FIELD, _("Single Line Text Field")),
        (TEXT_AREA, _("Multiple Lines Text Area")),
        (BOOLEAN_CHECKBOXES, _("Boolean with Checkbox")),
        (BOOLEAN_BUTTONS, _("Boolean with Buttons")),
        (SELECT_DROPDOWN, _("Select with Dropdown")),
        (SELECT_RADIO_BUTTONS, _("Select with Radio Buttons")),
        (SELECT_BUTTONS, _("Select with Buttons")),
        (SELECT_MULTIPLE_CHECKBOXES, _("Select Multiple with Checkboxes")),
        (SELECT_MULTIPLE_AUTOSUGGEST, _("Select Multiple with Autosuggest")),
        (SELECT_MULTIPLE_HORIZONTAL, _("Select Multiple with Horizontal Lists")),
        (FORM_INSTRUCTIONS, _("Form Instructions")),
        (FORM_DIVIDER, _("Form Divider")),
        (FORM_STEP, _("Form Step"))
    )

    type = models.CharField(max_length=255, choices=FORM_FIELD_CHOICES, 
        help_text=help['type'])

    parent = models.ForeignKey('form.Form', null=True, blank=True)

    order = models.IntegerField(default=0, help_text=help['order']) 

    secondary_label = models.CharField(max_length=255, null=True, 
        blank=True, help_text=help['secondary_label'])
    placeholder_text = models.CharField(max_length=255, null=True, 
        blank=True, help_text=help['placeholder_text'])
    help_text = models.CharField(max_length=255, null=True, 
        blank=True, help_text=help['help_text'])

    content = models.TextField(null=True, blank=True, help_text=help['content'])
    
    choices = models.TextField(null=True, blank=True, help_text=help['choices'])

    default = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['default'])


    class Meta:
        abstract = True
