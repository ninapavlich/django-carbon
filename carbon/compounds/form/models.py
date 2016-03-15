import cStringIO
from PIL import Image
import re
import ast
from dateutil.parser import parse as parsedate

from django import forms
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.urlresolvers import reverse_lazy
from django.core.validators import validate_email, URLValidator
from django.utils.translation import ugettext_lazy as _



from carbon.utils.slugify import unique_slugify
from carbon.utils.icons import ICON_CHOICES

from carbon.atoms.models.abstract import *
from carbon.atoms.models.content import *

from carbon.atoms.models.media import BaseSecureAtom

from .widgets import *
from .utils import *


# class FormClass(VersionableAtom, TitleAtom):
#   class Meta:
#       abstract = True




class Form(ContentMolecule):
    field_model = None
    help = {
        
        'admin_email':"",
        'email_admin_override':"Separate email addresses with comma, semi-color or space. Leave blank to send to default email address (%s)"%(settings.DEFAULT_FROM_EMAIL),
        'email_admin_on_submission':"",
        'email_admin_on_submission_template':"",
        'email_admin_on_submission_category':"",
        'email_user_field_slug':"Enter the slug of the field that should be used to determine the user's email address",
        'email_user_on_submission_template':"",
        'email_user_on_submission_category':"",
        'submission_content':"",
        'submit_template':"",

        'redirect_url_on_submission':"When a form is submitted you may override where the user is redirected.",
        'form_action': "Defines whether to display this form on its own page with its own URL, or whether to embed it on another page elsehwere in the site. NOTE: Several of the subsections below only apply if the form action is a standalone form.",
        'required_logged_in_user':"Requires user to log in or create an account before filling out form. NOTE: This should only be turned on if you have enabled user registration on the site.",
        'is_editable':"Allows user to update the entry. NOTE: If this is checked, unless you also require a logged in user on the form, anyone with the correct URL can later update the entry. Therefore it is recommended that you use this in conjunction with requiring a logged in user.",
        
        'submit_label':"Label on the submit button.",
        'form_error_message':"Global message to show user when there is an error in the form. NOTE: Individual fields have separate error messages.",
        'form_create_message':"Message to show user when they successfully submit the form.",
        'form_update_message':"Message to show user when they successfully update the form. NOTE: Form must be editable to allow users to update the form.",

        'extra_css_classes':"Adds custom css classes into the form template.",
        'third_party_id': "An identifier to integrate the form with another system",
    }

    POST_TO_FORM_PAGE = 'form-page'
    POST_TO_EMBEDDED_PAGE = 'embedded-page'
    FORM_ACTION_CHOICES = (
        (POST_TO_FORM_PAGE, _("Standalone Form")),
        (POST_TO_EMBEDDED_PAGE, _("Form Embedded in Page"))
    )

    form_action = models.CharField(max_length=255, choices=FORM_ACTION_CHOICES, 
        default=POST_TO_FORM_PAGE, help_text=help['form_action'])

    required_logged_in_user = models.BooleanField(default=False, 
        help_text=help['required_logged_in_user'])

    is_editable = models.BooleanField(default=False, 
        help_text=help['is_editable'])


    email_admin_override = models.CharField(_('Admins to email on submission'), null=True, blank=True, 
        max_length=255,help_text=help['email_admin_override'])
    email_admin_on_submission = models.BooleanField(default=True, 
        help_text=help['email_admin_on_submission'])
    email_admin_on_submission_template = models.ForeignKey(settings.EMAIL_TEMPLATE_MODEL, 
        null=True, blank=True, help_text=help['email_admin_on_submission_template'],
       related_name='email_admin_on_submission_template')
    admin_email = models.EmailField(max_length=255, blank=True, null=True,
        help_text=help['admin_email'])
    email_admin_on_submission_category = models.ForeignKey(settings.EMAIL_CATEGORY_MODEL, 
        null=True, blank=True, help_text=help['email_admin_on_submission_category'],
        related_name='email_admin_on_submission_category')


    email_user_field_slug = models.CharField(null=True, blank=True, 
        max_length=255,help_text=help['email_user_field_slug'])
    email_user_on_submission = models.BooleanField(default=True, 
        help_text=help['email_admin_on_submission'])
    email_user_on_submission_template = models.ForeignKey(settings.EMAIL_TEMPLATE_MODEL, 
        null=True, blank=True, help_text=help['email_user_on_submission_template'],
        related_name='email_user_on_submission_template')
    email_user_on_submission_category = models.ForeignKey(settings.EMAIL_CATEGORY_MODEL, 
        null=True, blank=True, help_text=help['email_user_on_submission_category'],
        related_name='email_user_on_submission_category')

    redirect_url_on_submission = models.CharField(max_length=255, null=True, 
        blank=True, help_text=help['redirect_url_on_submission'])

    submit_template = models.ForeignKey(settings.TEMPLATE_MODEL, null=True, blank=True,
        help_text=help['submit_template'], related_name='template_submit_template')   

    submission_content = models.TextField(help_text=help['submission_content'], 
        null=True, blank=True)

    submit_label = models.CharField(max_length=255, default="Submit",
        help_text=help['submit_label'])


    form_error_message = models.CharField(max_length=255, blank=True, null=True,
        help_text=help['form_error_message'])
    form_create_message = models.CharField(max_length=255, blank=True, null=True,
        help_text=help['form_create_message'])
    form_update_message = models.CharField(max_length=255, blank=True, null=True,
        help_text=help['form_update_message'])



    extra_css_classes = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['extra_css_classes'])

    third_party_id = models.CharField(max_length=255, blank=True, null=True,
        help_text=help['third_party_id'])

    def get_success_url(self, entry=None):
        if self.redirect_url_on_submission:
            return self.redirect_url_on_submission
        else:
            if self.is_editable and entry != None:
                return entry.get_absolute_url()
            else:
                return reverse('form_submitted_view', kwargs = {'path': self.slug }) 

    def handle_successful_submission(self, form, entry, created):
        if created:
            
            input_fields = self.get_input_fields()
            fields = []
            fields_dict = {}

            field_entry_hash = {}
            field_entries = entry.get_entries()
            for field_entry in field_entries:
                field_entry_hash[field_entry.form_field.slug] = field_entry

            #POPULATE KEY/VALUE PAIR:
            for field in input_fields:
                field_entry = field_entry_hash[field.slug]
                object = {
                    'title':field.title,
                    'value':field_entry.value,
                    'rendered_value':field_entry.get_rendered_value(),
                    'is_honeypot':field.is_honeypot,
                    'entry':field_entry, 
                    'field':field
                }
                fields.append(object)
                fields_dict[field.slug] = object

            context = {
                'input_fields':input_fields,
                'all_fields':self.get_all_fields(),
                'submitted_fields':fields,
                'submitted_fields_dict':fields_dict,
                'entry':entry,
                'form':self
            }

            if self.email_admin_on_submission:

                if not self.email_admin_on_submission_template:
                    raise ImproperlyConfigured( "Form is set to email admin on submission, but email admin template not specified" )

                if not self.email_admin_on_submission_category:
                    raise ImproperlyConfigured( "Form is set to email admin on submission, but email admin category not specified" )

                admin_email_list = self.get_admin_emails()
                for admin_email in admin_email_list:
                    self.email_admin_on_submission_template.send_email_message(admin_email, self.email_admin_on_submission_category, context)
            
            if self.email_user_on_submission:
                user_email_field = self.get_email_recipient_field()
                if user_email_field==None:
                    raise ImproperlyConfigured( "User recipient field not found" )
                
                user_email_entry = entry.get_entry_by_slug(user_email_field.slug)
                if user_email_entry:
                    if not self.email_user_on_submission_template:
                        raise ImproperlyConfigured( "Form is set to email user on submission, but email user template not specified" )

                    if not self.email_user_on_submission_category:
                        raise ImproperlyConfigured( "Form is set to email user on submission, but email user category not specified" )

                    self.email_user_on_submission_template.send_email_message(user_email_field, 
                            self.email_user_on_submission_category, context)

    def get_admin_emails(self):
        if self.email_admin_override:
            return re.split('; |, ',self.email_admin_override)
        return [settings.DEFAULT_FROM_EMAIL]

    def get_field_by_slug(self, slug):
        try:
          return self.field_model.objects.get(parent=self,slug=slug)
        except:
          return None

    def get_all_fields(self):
        return self.field_model.objects.filter(parent=self).exclude(hide=True).order_by('order')

    def get_input_fields(self):
        return self.field_model.objects.filter(parent=self).exclude(hide=True).exclude(
            Q(type=FormField.FORM_INSTRUCTIONS) | 
            Q(type=FormField.FORM_DIVIDER) |
            Q(type=FormField.FORM_STEP)
        ).order_by('order')

    def get_email_recipient_field(self):
        #TODO -- allow admin to specify which field is the email field

        if self.email_user_field_slug:
            fields = self.get_all_fields()
            email_fields = fields.filter(slug=self.email_user_field_slug)
            if len(email_fields) > 0:
                return email_fields[0]
        

        email_fields = self.field_model.objects.filter(parent=self).exclude(hide=True).filter(
            type=FormField.EMAIL_FIELD
        ).order_by('order')
        if len(email_fields) > 0:
            return email_fields[0]
        
        return None

    def has_multipart(self):
        fields = self.get_all_fields().filter(
            Q(type=FormField.FILE) | 
            Q(type=FormField.SECURE_FILE) | 
            Q(type=FormField.IMAGE)
        )
        return len(fields) > 0

    def get_form_action(self):
        if self.form_action == Form.POST_TO_FORM_PAGE:
            return self.get_absolute_url()
        else:
            return '.'

    def get_absolute_url(self):
        if self.form_action == Form.POST_TO_FORM_PAGE:
            return reverse('form_create_view', kwargs = {'path': self.slug }) 
        else:
            return None
        

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Forms"
        verbose_name = "Forms"
        abstract = True



class Validation(models.Model):
    #Maps to http://parsleyjs.org/doc/index.html#psly-validators-overview
    help = {
        'is_required':"If this field is required, a value of some sort is needed for the user to submit the form. See the advanced validation options to apply more specific validation parameters.",
        'is_digits':"",
        'is_alphanumeric':"",
        'min_length':"",
        'max_length':"",
        'min_words':"",
        'max_words':"",
        'min_value':"",
        'max_value':"",
        'min_check':"",
        'max_check':"",     
        'min_date':"",
        'max_date':"",
        'min_datetime':"",
        'max_datetime':"",
        'min_width':"Applies to image uploads",
        'max_width':"Applies to image uploads",
        'min_height':"Applies to image uploads",
        'max_height':"Applies to image uploads",
        'min_size':"Applies to image and file uploads, measured in MB; e.g. 5000 is 5GB, 0.5 is 500KB",
        'max_size':"Applies to image and file uploads, measure in MB; e.g. 5000 is 5GB, 0.5 is 500KB",
        'pattern':"Match a value or validate file types (e.g. .*\.txt|.*\.pdf|.*\.doc)",
        'equal_to':"Enter form field slug that this field should match",
        'step_interval':"If values is a score, range, or slider, pick the step interval."
    }


    
    is_required = models.BooleanField(default=False, 
        help_text=help['is_required'])
    is_digits = models.BooleanField(default=False, 
        help_text=help['is_digits'])
    is_alphanumeric = models.BooleanField(default=False, 
        help_text=help['is_alphanumeric'])


    min_length = models.IntegerField(null=True, blank=True, help_text=help['min_length']) 
    max_length = models.IntegerField(null=True, blank=True, help_text=help['max_length']) 
    min_words = models.IntegerField(null=True, blank=True, 
        help_text=help['min_words'])
    max_words = models.IntegerField(null=True, blank=True, 
        help_text=help['max_words'])


    min_value = models.IntegerField(null=True, blank=True, help_text=help['min_value']) 
    max_value = models.IntegerField(null=True, blank=True, help_text=help['max_value'])

    min_check = models.IntegerField(null=True, blank=True, help_text=help['min_check']) 
    max_check = models.IntegerField(null=True, blank=True, help_text=help['max_check'])  
    

    min_date = models.DateField(blank=True, null=True, 
        help_text=help['min_date'])
    max_date = models.DateField(blank=True, null=True, 
        help_text=help['max_date'])
    min_datetime = models.DateTimeField(blank=True, null=True, 
        help_text=help['min_datetime'])
    max_datetime = models.DateTimeField(blank=True, null=True, 
        help_text=help['max_datetime'])

    min_width = models.IntegerField(null=True, blank=True, 
        help_text=help['min_width'])
    max_width = models.IntegerField(null=True, blank=True, 
        help_text=help['max_width'])
    min_height = models.IntegerField(null=True, blank=True, 
        help_text=help['min_height'])
    max_height = models.IntegerField(null=True, blank=True, 
        help_text=help['max_height'])
    min_size = models.IntegerField(null=True, blank=True, 
        help_text=help['min_size'])
    max_size = models.IntegerField(null=True, blank=True, 
        help_text=help['max_size'])

    
    step_interval = models.DecimalField(null=True, blank=True, help_text=help['step_interval'],
        max_digits=9, decimal_places=2) 

    pattern = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['pattern'])
    pattern_error_message = models.CharField(max_length=255, null=True, blank=True)

    equal_to = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['equal_to'])
    equal_to_error_message = models.CharField(max_length=255, null=True, blank=True)


    def validate(self, value, form):
        if value:
            # if self.is_required and not value:
            #     raise ValidationError(_("This field is required"))  

            if self.type == FormField.HONEYPOT_FIELD:
                raise ValidationError(_("Please try again"))

            if self.type == FormField.INTEGER_FIELD and not is_int(value):
                raise ValidationError(_("Please enter an integer"))

            # if self.type == FormField.NUMBER_FIELD and not value.isdigit():
            #     raise ValidationError(_("Please enter a number"))
        
            if self.is_digits and not value.isdigit():
              raise ValidationError(_("Please enter numeric digits only"))

            if self.is_alphanumeric and not value.isalnum():
              raise ValidationError(_("Please enter leters and numbers only"))

            if self.min_length and not len(value) >= self.min_length:
              raise ValidationError(_("Please enter at least %s characters"%(self.min_length)))

            if self.max_length and not len(value) <= self.max_length:
              raise ValidationError(_("Please enter no more than %s characters"%(self.max_length)))

            if self.min_words and not len(value.split()) >= self.min_words:
              raise ValidationError(_("Please enter at least %s words"%(self.min_words)))

            if self.max_words and not len(value.split()) <= self.max_words:
              raise ValidationError(_("Please enter no more than %s characters"%(self.max_words)))

            if self.min_value and not float(value) >= self.min_value:
              raise ValidationError(_("Please enter a value of %s or greater"%(self.min_value)))

            if self.max_value and not float(value) <= self.max_value:
              raise ValidationError(_("Please enter a value of %s or less"%(self.max_value)))

            if self.type == FormField.DATE or self.type == FormField.DATE_TIME:
              date = parsedate(value).date()
              if self.min_date and not date >= self.min_date:
                raise ValidationError(_("Please enter a date of %s or later"%(self.min_date)))
              if self.max_date and not date <= self.max_date:
                raise ValidationError(_("Please enter a date of %s or earlier"%(self.max_date)))

                if self.type == FormField.DATE_TIME:
                    if self.min_datetime and not date >= self.min_datetime:
                      raise ValidationError(_("Please enter a date and time of %s or later"%(self.min_datetime)))
                    if self.max_datetime and not date <= self.max_datetime:
                      raise ValidationError(_("Please enter a date and time of %s or earlier"%(self.max_datetime)))

            if self.type == FormField.EMAIL_FIELD:
                validate_email(value)

            if self.type == FormField.URL_FIELD:
                validator = URLValidator()
                validator(value)





            if self.is_multipart and value:
              
              if self.min_size and not (self.min_size * 1024 * 1024) <= value.size:
                raise ValidationError(_("Please select a file that is %sMB or larger"%(self.min_size)))

              if self.max_size and not (self.max_size * 1024 * 1024) >= value.size:
                raise ValidationError(_("Please select a file that is %sMB or smaller"%(self.max_size)))

            # if self.type==FormField.IMAGE and value:
              

            #   if self.min_width or self.max_width or self.min_height or self.max_height:

            #     if isinstance(value, TemporaryUploadedFile):
            #       temp_file = open(value.temporary_file_path(), 'rb+')
            #       content = cStringIO.StringIO(temp_file.read())
            #       image = Image.open(content)
            #       width, height = image.size
            #     else:
            #       # print value.read()
            #       # print value.file.read()
            #       # content = cStringIO.StringIO(value.read())
            #       image = Image.open(value.read())
            #       width, height = image.size

            #     if self.min_width and not self.min_width <= width:
            #       raise ValidationError(_("Please select an image that is %spx wide or more"%(self.min_width)))

            #     if self.max_width and not self.max_width >= width:
            #       raise ValidationError(_("Please select an image that is %spx wide or less"%(self.max_width)))

            #     if self.min_height and not self.min_height <= height:
            #       raise ValidationError(_("Please select an image that is %spx tall or more"%(self.min_height)))

            #     if self.max_height and not self.max_height >= height:
            #       raise ValidationError(_("Please select an image that is %spx tall or less"%(self.max_height)))
                


            if self.equal_to:
              key = 'form_field_%s'%(self.equal_to)
              equal_value = form._raw_value(key)
              if not equal_value:
                field = self.form.get_field_by_slug(key)
                if field:
                    equal_value = field.default
              if not value == equal_value:
                raise ValidationError(self.equal_to_error_message)

            if self.pattern:
              if value:
                  
                test = value
                if isinstance(value, InMemoryUploadedFile) or isinstance(value, TemporaryUploadedFile):
                  test = value.name

                # print self.pattern
                # print test
                # print self.pattern.decode('string_escape')

                result = re.match(self.pattern, test)
                if not result:
                  raise ValidationError(self.pattern_error_message)



    class Meta:

        abstract = True

class FormField(VersionableAtom, TitleAtom, Validation):

    help = {
        'order': "",
        'type':"Fill in choices field (in advanced options) for select fields. Fill in content field for instructions. WARNING: Only use password and secure file in conjunction with HTTPS.",
        'secondary_label':"",
        'placeholder_text':"",
        'help_text':"",
        'content':"Rich-text instructions",
        'default':"Default field value",
        'extra_css_classes':"Adds custom css classes onto the form field in the template.",
        'hide':"Hide field from form without deleting and data entered by users. Use this instead of deleting a form field.",
        'icon_right':'Add icon to the right side of the field. Preview icons at http://fontawesome.io/icons/',
        'icon_left':'Add icon to the left side of the field. Preview icons at http://fontawesome.io/icons/',
        'inset_text_right':"Inset field with content on the right",
        'inset_text_left':"Inset field with content on the left",
        'error_message':"Message to display when this field is invalid.",
        'third_party_id': "An identifier to integrate the form with another system",
        'choices':"Comma separated options where applicable. If an option "
            "itself contains commas, surround the option starting with the %s"
            "character and ending with the %s character." %
                (settings.FORM_CHOICES_QUOTE, settings.FORM_CHOICES_UNQUOTE)
    }



    TEXT_FIELD = 'text-field'
    EMAIL_FIELD = 'email-field'
    URL_FIELD = 'url-field'
    INTEGER_FIELD = 'integer-field'
    NUMBER_FIELD = 'number-field'
    TEXT_AREA = 'text-area'
    BOOLEAN_CHECKBOXES = 'boolean-checkboxes'
    BOOLEAN_TOGGLE = 'boolean-toggle'
    SELECT_DROPDOWN = 'select-dropdown'
    SELECT_RADIO_BUTTONS = 'select-radio-buttons'
    SELECT_BUTTONS = 'select-buttons'
    SELECT_IMAGE = 'select-image'
    SELECT_MULTIPLE_CHECKBOXES = 'select-multiple-checkboxes'
    SELECT_MULTIPLE_AUTOSUGGEST = 'select-multiple-autosuggest'
    SELECT_MULTIPLE_HORIZONTAL = 'select-multiple-horizontal'
    SELECT_MULTIPLE_BUTTONS = 'select-multiple-buttons'
    SELECT_MULTIPLE_IMAGES = 'select-multiple-images'
    COMMA_SEPARATED_LIST = 'comma-separated-list'
    FILE = 'file'
    SECURE_FILE = 'secure-file'
    IMAGE = 'image'
    DATE = 'date'
    TIME = 'time'
    DATE_TIME = 'date-time'
    SCORE = 'score'
    RANGE = 'range'
    NUMBER_SLIDER = 'number-slider'
    PASSWORD = 'password'

    FORM_INSTRUCTIONS = 'form-instructions'
    FORM_DIVIDER = 'form-divider'
    FORM_STEP = 'form-step'
    HIDDEN_FIELD = 'hidden-field'
    HONEYPOT_FIELD = 'honeypot-field'

        
    FORM_FIELD_CHOICES = (
        (TEXT_FIELD, _("Single Line Text Field")),
        (EMAIL_FIELD, _("Email Field")),
        (URL_FIELD, _("URL Field")),
        (INTEGER_FIELD, _("Integer Field")),
        (NUMBER_FIELD, _("Number Field")),
        (TEXT_AREA, _("Multiple Lines Text Area")),
        (BOOLEAN_CHECKBOXES, _("Single Checkbox")),
        (BOOLEAN_TOGGLE, _("Toggle")),
        (SELECT_DROPDOWN, _("Select with Dropdown")),
        (SELECT_RADIO_BUTTONS, _("Select with Radio Buttons")),
        (SELECT_BUTTONS, _("Select with Buttons")),
        (SELECT_IMAGE, _("Select Image")),
        (SELECT_MULTIPLE_CHECKBOXES, _("Select Multiple with Checkboxes")),
        (SELECT_MULTIPLE_AUTOSUGGEST, _("Select Multiple with Autosuggest")),
        (SELECT_MULTIPLE_HORIZONTAL, _("Select Multiple with Horizontal Lists")),   
        (SELECT_MULTIPLE_BUTTONS, _("Select Multiple with Buttons")),
        (SELECT_MULTIPLE_IMAGES, _("Select Multiple Images")),  
        (COMMA_SEPARATED_LIST, _("List of Items")),  
        (FILE, _("File")),
        (SECURE_FILE, _("Secure File")),
        (IMAGE, _("Image")),
        (DATE, _("Date")),
        (TIME, _("Time")),
        (DATE_TIME, _("Date and Time")),
        (SCORE, _("Score")),
        (RANGE, _("Range")),
        (NUMBER_SLIDER, _("Number on a Slider")),
        (PASSWORD, _("Password")),
        (FORM_INSTRUCTIONS, _("Form Instructions")),
        (FORM_DIVIDER, _("Form Divider")),
        (FORM_STEP, _("Form Step")),
        (HIDDEN_FIELD, _("Hidden Field")),
        (HONEYPOT_FIELD, _("Honeypot Field"))
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

    extra_css_classes = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['extra_css_classes'])

    icon_right = models.CharField(max_length=255, null=True, blank=True, 
        choices=ICON_CHOICES, help_text=help['icon_right'])
    icon_left = models.CharField(max_length=255, null=True, blank=True, 
        choices=ICON_CHOICES, help_text=help['icon_left'])
    inset_text_right = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['inset_text_right'])
    inset_text_left = models.CharField(max_length=255, null=True, blank=True, 
        help_text=help['inset_text_left'])

    hide = models.BooleanField(default=False, help_text=help['hide'])

    error_message = models.CharField(max_length=255, blank=True, null=True,
        help_text=help['error_message'])

    third_party_id = models.CharField(max_length=255, blank=True, null=True,
        help_text=help['third_party_id'])

    def get_choices(self):
        raw_choices = self.choices.split(',')
        choices = tuple((n,n) for n in raw_choices)     
        return choices

    @property
    def is_multipart(self):
        return (self.type==FormField.FILE or self.type==FormField.SECURE_FILE or self.type==FormField.IMAGE)

    @property
    def input_type(self):
        return get_form_field_input_type_by_type(self.type)

    def get_form_field(self):
        return get_form_field_by_type(self.type, self, self.title, self.get_choices())

    @property
    def is_honeypot(self):
        if self.type == FormField.HONEYPOT_FIELD:
            return True
        return False

    def compress(self, raw_value):
    #PYTHON -> DATABASE
        if self.type == FormField.SELECT_MULTIPLE_CHECKBOXES or \
            self.type == FormField.SELECT_MULTIPLE_AUTOSUGGEST or \
            self.type == FormField.SELECT_MULTIPLE_HORIZONTAL or \
            self.type == FormField.SELECT_MULTIPLE_BUTTONS or \
            self.type == FormField.SELECT_MULTIPLE_IMAGES:

           
            if len(raw_value)==0:
                value = ''
            else:
                is_list = isinstance(raw_value, (list, tuple))

                if not is_list:
                    #SUSS OUT VALUE -- not sure what this does -nina
                    # if(len(raw_value)>0):
                    #     first_element = raw_value[0]
                    #     print 'frst element? %s'%(first_element)
                    #     if isinstance(first_element, (list)):
                    #         raw_value = first_element
                    unescaped = unescape(raw_value)
                    as_list = ast.literal_eval(unescaped.strip())
                    value = ', '.join(as_list)

                else:
                    value = ', '.join(raw_value)

            # print 'python->DB value %s -> %s'%(raw_value, value)
        else:
            value = raw_value
        
        return value

    def decompress(self, raw_value):
    #DATABASE -> PYTHON
        if self.type == FormField.SELECT_MULTIPLE_CHECKBOXES or \
            self.type == FormField.SELECT_MULTIPLE_AUTOSUGGEST or \
            self.type == FormField.SELECT_MULTIPLE_HORIZONTAL or \
            self.type == FormField.SELECT_MULTIPLE_BUTTONS or \
            self.type == FormField.SELECT_MULTIPLE_IMAGES:

            

            if isinstance(raw_value, basestring):
                if raw_value=='':
                    value = []
                else:
                    value = raw_value.split(', ')
                    # print 'decompress Raw value = %s; value = %s'%(raw_value, value)
            else:
                #already formatted
                value = raw_value

            # print 'DB->python value %s -> %s'%(raw_value, value)
        else:
            value = raw_value


        
        return value

    

    def generate_slug(self):
        starting_slug = '%s-%s'%(self.parent.slug, self.title)
        unique_slugify(self, starting_slug)
        return self.slug

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Form Fields"
        verbose_name = "Form Field"
        abstract = True



class FormEntry(VersionableAtom):

    form_schema = models.ForeignKey('form.Form', null=True, blank=True)

    NEW = 'new'
    READ = 'read'
    REPLIED = 'replied'
    ARCHIVED = 'archived'
    FORM_ENTRY_STATUS_CHOICES = (
        (NEW, _("New")),
        (READ, _("Read")),
        (REPLIED, _("Replied")),
        (ARCHIVED, _("Archived")),
    )

    status = models.CharField(choices=FORM_ENTRY_STATUS_CHOICES, 
        default=NEW, max_length = 255)

    tags = models.ManyToManyField('form.FormEntryTag', blank=True)

    def get_absolute_url(self):
        if self.form_schema.is_editable:
            return reverse('form_update_view', kwargs = {'path': self.form_schema.slug, 'pk':self.pk }) 
        return None

    def get_entry_by_slug(self, slug):
        try:
          return self.field_entry_model.objects.get(form_entry=self,form_field__slug=slug)
        except:
          return None

    def get_fields_with_entries(self):
        field_entry_hash = {}
        field_entries = self.get_entries()
        for field_entry in field_entries:
            field_entry_hash[field_entry.form_field.slug] = field_entry

        input_fields = self.form_schema.get_input_fields()

        #POPULATE KEY/VALUE PAIR:
        fields = []
        for field in input_fields:
            if field.slug in field_entry_hash:
                field_entry = field_entry_hash[field.slug]
                object = {'title':field.title,'value':field_entry.value,'entry':field_entry, 'field':field}
                fields.append(object)

        return fields


    def get_entries(self):
        return self.field_entry_model.objects.filter(form_entry=self).order_by('form_field__order')


    class Meta:
        abstract = True
        verbose_name = "Form Entry"
        verbose_name_plural = "Form Entries"


class FieldEntry(VersionableAtom):

    form_entry = models.ForeignKey('form.FormEntry', null=True, blank=True)
    form_field = models.ForeignKey('form.FormField', null=True, blank=True)
    
    value = models.TextField(null=True, blank=True)

    @property
    def decompressed_value(self):
    #DATABASE -> PYTHON
        return self.form_field.decompress(self.value)

    def get_compressed_value(self, value):
    #PYTHON -> DATABASE
        return self.form_field.compress(value)

    def get_rendered_value(self):
        if self.decompressed_value:
          if self.form_field.is_multipart:      
            file_url = "%s%s"%(settings.MEDIA_URL, self.value)
            if self.form_field.type==FormField.IMAGE:
                return '<img src="%s" >'%(file_url)
            elif self.form_field.type==FormField.FILE:
                return '<a href="%s" target="_blank">%s</a>'%(file_url, self.value)
            elif self.form_field.type==FormField.SECURE_FILE:
                duration = 120
                key_name = "%s/%s"%(settings.AWS_MEDIA_FOLDER, self.value)
                file_url = BaseSecureAtom.generate_link(settings.AWS_STORAGE_BUCKET_NAME_MEDIA_SECURE, key_name, duration)
                return '<a href="%s" target="_blank">%s</a><br /><br />This link will expire after %s seconds.</a>'%(file_url, self.value, duration)

            else:
                return file_url

          return self.value
        return ''

    
        
    
    class Meta:
        abstract = True
        verbose_name_plural = "Field Entries"
        verbose_name = "Field Entry"
        ordering = ['form_field__order']


class FormEntryStatus(CategoryMolecule):
    publish_by_default = True
    # default_template = 'media_tag'
    # item_classes = [Image, Media, SecureImage, SecureMedia]
    
    class Meta:
        verbose_name_plural = "Form Entry Statuses"
        verbose_name = "Form Entry Status"
        abstract = True

class FormEntryTag(TagMolecule):
    publish_by_default = True
    # default_template = 'media_tag'
    # item_classes = [Image, Media, SecureImage, SecureMedia]
    
    class Meta:
        verbose_name_plural = "Form Entry Tags"
        verbose_name = "Form Entry Tag"
        abstract = True        



def is_int(value):
    try: 
        int(value)
        return True
    except ValueError:
        return False

def unescape(value):
    from htmlentitydefs import name2codepoint
    # for some reason, python 2.5.2 doesn't have this one (apostrophe)
    name2codepoint['#39'] = 39

    return re.sub('&(%s);' % '|'.join(name2codepoint),
              lambda m: unichr(name2codepoint[m.group(1)]), value)

