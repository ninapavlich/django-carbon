from django import forms
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


from carbon.utils.slugify import unique_slugify

from carbon.atoms.models.abstract import *
from carbon.atoms.models.content import *

class Form(ContentMolecule):
	field_model = None
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

	def get_all_fields(self):
		return self.field_model.objects.filter(parent=self).order_by('order')

	def get_input_fields(self):
		return self.field_model.objects.filter(parent=self).exclude(
			Q(type=FormField.FORM_INSTRUCTIONS) | 
			Q(type=FormField.FORM_DIVIDER) |
			Q(type=FormField.FORM_STEP)
		).order_by('order')

	def get_absolute_url(self):
		return reverse('form_create_view', kwargs = {'path': self.slug }) 

	class Meta:
		abstract = True



class Validation(models.Model):
	#Maps to http://parsleyjs.org/doc/index.html#psly-validators-overview
	help = {
		'is_email': "",
		'is_required':"",
		'is_number':"",
		'is_integer':"",
		'is_digits':"",
		'is_alphanumeric':"",
		'is_url':"",
		'min_length':"",
		'max_length':"",
		'min_value':"",
		'max_value':"",
		'pattern':"",
		'min_check':"",
		'max_check':"",
		'equal_to':"Enter form field slug that this field should match",
		'min_date':"",
		'max_date':"",
		'min_words':"",
		'max_words':""
	}



	is_email = models.BooleanField(default=False, 
		help_text=help['is_email'])
	is_required = models.BooleanField(default=False, 
		help_text=help['is_required'])
	is_number = models.BooleanField(default=False, 
		help_text=help['is_number'])
	is_integer = models.BooleanField(default=False, 
		help_text=help['is_integer'])
	is_digits = models.BooleanField(default=False, 
		help_text=help['is_digits'])
	is_alphanumeric = models.BooleanField(default=False, 
		help_text=help['is_alphanumeric'])
	is_url = models.BooleanField(default=False, 
		help_text=help['is_url'])

	min_length = models.IntegerField(null=True, blank=True, help_text=help['min_length']) 
	max_length = models.IntegerField(null=True, blank=True, help_text=help['max_length']) 
	min_value = models.IntegerField(null=True, blank=True, help_text=help['min_value']) 
	max_value = models.IntegerField(null=True, blank=True, help_text=help['max_value']) 

	pattern = models.CharField(max_length=255, null=True, blank=True, 
		help_text=help['pattern'])

	min_check = models.IntegerField(null=True, blank=True, help_text=help['min_check']) 
	max_check = models.IntegerField(null=True, blank=True, help_text=help['max_check']) 

	equal_to = models.CharField(max_length=255, null=True, blank=True, 
		help_text=help['equal_to'])


	#EXTRA
	min_date = models.DateField(blank=True, null=True, 
		help_text=help['min_date'])
	max_date = models.DateField(blank=True, null=True, 
		help_text=help['max_date'])
	min_words = models.IntegerField(null=True, blank=True, 
		help_text=help['min_words'])
	max_words = models.IntegerField(null=True, blank=True, 
		help_text=help['max_words'])




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
		'hide':"Hide field from form without deleting and data entered by users",
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
	FILE = 'file'
	SECURE_FILE = 'secure-file'
	DATE = 'date'
	TIME = 'time'
	DATE_TIME = 'date-time'

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
		(FILE, _("File")),
		(SECURE_FILE, _("Secure File")),
		(DATE, _("Date")),
		(TIME, _("Time")),
		(DATE_TIME, _("Date and Time")),
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


	hide = models.BooleanField(default=False, help_text=help['hide'])

	def get_choices(self):
		raw_choices = self.choices.split(',')
		return raw_choices

	def get_widget(self):
		field = None

		if self.type == FormField.TEXT_FIELD:

			if self.is_email:
				field = forms.EmailField(label=self.title)
			elif self.is_url:
				field = forms.CharField(label=self.title)
			elif self.is_integer:
				field = forms.IntegerField(label=self.title)
			elif self.is_number:
				field = forms.DecimalField(label=self.title)
			else:
				field = forms.CharField(label=self.title)


		elif self.type == FormField.TEXT_AREA:
			field = forms.CharField(label=self.title)

		elif self.type == FormField.BOOLEAN_CHECKBOXES:
			field = forms.BooleanField(label=self.title)

		elif self.type == FormField.BOOLEAN_BUTTONS:				
			field = forms.BooleanField(label=self.title)

		elif self.type == FormField.SELECT_DROPDOWN:
			field = forms.ChoiceField(label=self.title, choices=self.get_choices())

		elif self.type == FormField.SELECT_RADIO_BUTTONS:
			field = forms.ChoiceField(label=self.title, choices=self.get_choices())

		elif self.type == FormField.SELECT_BUTTONS:
			field = forms.ChoiceField(label=self.title, choices=self.get_choices())

		elif self.type == FormField.SELECT_MULTIPLE_CHECKBOXES:
			field = forms.MultipleChoiceField(label=self.title, choices=self.get_choices())

		elif self.type == FormField.SELECT_MULTIPLE_AUTOSUGGEST:
			field = forms.MultipleChoiceField(label=self.title, choices=self.get_choices())

		elif self.type == FormField.SELECT_MULTIPLE_HORIZONTAL:
			field = forms.MultipleChoiceField(label=self.title, choices=self.get_choices())

	
		elif self.type == FormField.FILE:
			field = forms.FileField(label=self.title)

		elif self.type == FormField.SECURE_FILE:
			field = forms.FileField(label=self.title)

		elif self.type == FormField.DATE:
			field = forms.DateField(label=self.title)

		elif self.type == FormField.TIME:
			field = forms.TimeField(label=self.title)

		elif self.type == FormField.DATE_TIME:
			field = forms.DateTimeField(label=self.title)

		# is_required = models.BooleanField(default=False, 
		#     help_text=help['is_required'])    
		# is_digits = models.BooleanField(default=False, 
		#     help_text=help['is_digits'])
		# is_alphanumeric = models.BooleanField(default=False, 
		#     help_text=help['is_alphanumeric'])
		# field.required = self.is_required    
		# field.secondary_label = self.secondary_label    
		# field.placeholder_text = self.placeholder_text    
		# field.help_text = self.help_text    

	
		return field

	def generate_slug(self):
		starting_slug = '%s-%s'%(self.parent.slug, self.title)
		unique_slugify(self, starting_slug)
		return self.slug

	class Meta:
		abstract = True


class FormEntry(VersionableAtom):

	form = models.ForeignKey('form.Form', null=True, blank=True)


	def get_absolute_url(self):
		path = "/%s/%s/" % (settings.FORMS_DOMAIN, self.form.slug)
		return reverse_lazy('form_update_view', kwargs = {'path': path, 'pk':self.pk }) 


	class Meta:
		abstract = True


class FieldEntry(VersionableAtom):

	entry = models.ForeignKey('form.FormEntry', null=True, blank=True)
	field = models.ForeignKey('form.FormField', null=True, blank=True)
	
	value = models.TextField(null=True, blank=True)

	@property
	def formatted_value(self):
		#value converted to format:
		#TODO
		return self.value
	
	class Meta:
		abstract = True
