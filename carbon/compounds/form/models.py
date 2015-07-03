from django import forms
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


from carbon.utils.slugify import unique_slugify
from carbon.utils.icons import ICON_CHOICES

from carbon.atoms.models.abstract import *
from carbon.atoms.models.content import *

from .widgets import *
from .utils import *


# class FormClass(VersionableAtom, TitleAtom):
# 	class Meta:
# 		abstract = True


class Form(ContentMolecule):
	field_model = None
	help = {
		'form_action': "Current publication status",
		'admin_email':"",
		'email_admin_override':"Leave blank to use default email address (%s)"%(settings.DEFAULT_FROM_EMAIL),
		'email_admin_on_submission':"",
		'email_admin_on_submission_template':"",
		'email_admin_on_submission_category':"",
		'email_user_field_slug':"Enter the slug of the field that should be used to determine the user's email address",
		'email_user_on_submission_template':"",
		'email_user_on_submission_category':"",
		'submission_content':"",
		'redirect_url_on_submission':"",
		'submit_label':"",
		'extra_css_classes':"",
		'submit_template':"",
		'required_logged_in_user':"",
		'is_editable':"",
		'form_error_message':"",
		'form_create_message':"",
		'form_update_message':""
	}

	POST_TO_FORM_PAGE = 'form-page'
	POST_TO_EMBEDDED_PAGE = 'embedded-page'
	FORM_ACTION_CHOICES = (
		(POST_TO_FORM_PAGE, _("Form Page")),
		(POST_TO_EMBEDDED_PAGE, _("Embedded Page"))
	)

	form_action = models.CharField(max_length=255, choices=FORM_ACTION_CHOICES, 
		default=POST_TO_FORM_PAGE, help_text=help['form_action'])

	required_logged_in_user = models.BooleanField(default=False, 
		help_text=help['required_logged_in_user'])

	is_editable = models.BooleanField(default=False, 
		help_text=help['is_editable'])


	email_admin_override = models.CharField(null=True, blank=True, 
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
				object = {'title':field.title,'value':field_entry.value,'entry':field_entry, 'field':field}
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

				self.email_admin_on_submission_template.send_email_message(settings.DEFAULT_FROM_EMAIL, 
					self.email_admin_on_submission_category, context)
			
			if self.email_user_on_submission:
				user_email_field = self.get_email_recipient_field()
				if user_email_field==None:
					raise ImproperlyConfigured( "User recipient field not found" )
				
				if not self.email_admin_on_submission_template:
					raise ImproperlyConfigured( "Form is set to email user on submission, but email user template not specified" )

				if not self.email_user_on_submission_category:
					raise ImproperlyConfigured( "Form is set to email user on submission, but email user category not specified" )

				self.email_user_on_submission_template.send_email_message(user_email_field, 
						self.email_user_on_submission_category, context)


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
			Q(type=FormField.SECURE_FILE)
		)
		return len(fields) > 0

	def get_form_action(self):
		if self.form_action == Form.POST_TO_FORM_PAGE:
			return self.get_absolute_url()
		else:
			return '.'

	def get_absolute_url(self):
		return reverse('form_create_view', kwargs = {'path': self.slug }) 

	def __unicode__(self):
		return self.title

	class Meta:
		abstract = True



class Validation(models.Model):
	#Maps to http://parsleyjs.org/doc/index.html#psly-validators-overview
	help = {
		'is_required':"",
		'is_digits':"",
		'is_alphanumeric':"",
		'min_length':"",
		'max_length':"",
		'min_value':"",
		'max_value':"",
		'min_check':"",
		'max_check':"",		
		'min_date':"",
		'max_date':"",
		'min_words':"",
		'max_words':"",
		'min_time':"",
		'max_time':"",
		'pattern':"",
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
	min_value = models.IntegerField(null=True, blank=True, help_text=help['min_value']) 
	max_value = models.IntegerField(null=True, blank=True, help_text=help['max_value'])
	min_check = models.IntegerField(null=True, blank=True, help_text=help['min_check']) 
	max_check = models.IntegerField(null=True, blank=True, help_text=help['max_check'])  
	
	#EXTRA
	min_date = models.DateField(blank=True, null=True, 
		help_text=help['min_date'])
	max_date = models.DateField(blank=True, null=True, 
		help_text=help['max_date'])
	min_time = models.DateField(blank=True, null=True, 
		help_text=help['min_time'])
	max_time = models.DateField(blank=True, null=True, 
		help_text=help['max_time'])
	min_words = models.IntegerField(null=True, blank=True, 
		help_text=help['min_words'])
	max_words = models.IntegerField(null=True, blank=True, 
		help_text=help['max_words'])

	step_interval = models.DecimalField(null=True, blank=True, help_text=help['step_interval'],
		max_digits=9, decimal_places=2)	

	pattern = models.CharField(max_length=255, null=True, blank=True, 
		help_text=help['pattern'])

	equal_to = models.CharField(max_length=255, null=True, blank=True, 
		help_text=help['equal_to'])


	



	class Meta:
		abstract = True

class FormField(VersionableAtom, TitleAtom, Validation):

	help = {
		'order': "",
		'type':"Fill in choices field (in advanced options) for select fields. Fill in content field for instructions.",
		'secondary_label':"",
		'placeholder_text':"",
		'help_text':"",
		'content':"Rich-text instructions",
		'default':"Default field value",
		'extra_css_classes':"",
		'hide':"Hide field from form without deleting and data entered by users",
		'icon_right':'Add icon to the right side of the field. Preview icons at http://fontawesome.io/icons/',
		'icon_left':'Add icon to the left side of the field. Preview icons at http://fontawesome.io/icons/',
		'inset_text_right':"Inset field with content on the right",
		'inset_text_left':"Inset field with content on the left",
		'error_message':"",
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
		(DATE, _("Date")),
		(TIME, _("Time")),
		(DATE_TIME, _("Date and Time")),
		(SCORE, _("Score")),
		(RANGE, _("Range")),
		(NUMBER_SLIDER, _("Number on a Slider")),
		(PASSWORD, _("Password")),
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

	def get_choices(self):
		raw_choices = self.choices.split(',')
		choices = tuple((n,n) for n in raw_choices)		
		return choices

	@property
	def input_type(self):
		return get_form_field_input_type_by_type(self.type)

	def get_form_field(self):
		return get_form_field_by_type(self.type, self, self.title, self.get_choices())

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

				#SUSS OUT VALUE
				if(len(raw_value)>0):
					first_element = raw_value[0]
					if isinstance(first_element, (list)):
						raw_value = first_element

				value = ','.join(raw_value)
				# print 'compress Raw value = %s; value = %s'%(raw_value, value)
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
					value = raw_value.split(',')
					# print 'decompress Raw value = %s; value = %s'%(raw_value, value)
			else:
				#already formatted
				value = raw_value
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
		return reverse('form_update_view', kwargs = {'path': self.form_schema.slug, 'pk':self.pk }) 

	def get_fields_with_entries(self):
		field_entry_hash = {}
		field_entries = self.get_entries()
		for field_entry in field_entries:
			field_entry_hash[field_entry.form_field.slug] = field_entry

		input_fields = self.form_schema.get_input_fields()

		#POPULATE KEY/VALUE PAIR:
		fields = []
		for field in input_fields:
			field_entry = field_entry_hash[field.slug]
			object = {'title':field.title,'value':field_entry.value,'entry':field_entry, 'field':field}
			fields.append(object)

		return fields


	def get_entries(self):
		return self.field_entry_model.objects.filter(form_entry=self).order_by('form_field__order')

	class Meta:
		abstract = True
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
		
	
	class Meta:
		abstract = True
		verbose_name_plural = "Field Entries"
		ordering = ['form_field__order']


class FormEntryStatus(CategoryMolecule):
    publish_by_default = True
    # default_template = 'media_tag'
    # item_classes = [Image, Media, SecureImage, SecureMedia]
    
    class Meta:
        abstract = True

class FormEntryTag(TagMolecule):
    publish_by_default = True
    # default_template = 'media_tag'
    # item_classes = [Image, Media, SecureImage, SecureMedia]
    
    class Meta:
        abstract = True        

