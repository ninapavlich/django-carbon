from .widgets import *

class FieldData(object):

	def __init__(self, is_required, secondary_label='', placeholder='', help_text=''):
		self.is_required = is_required
		self.secondary_label = secondary_label
		self.placeholder = placeholder
		self.help_text = help_text

		self.icon = None
		self.extra_css_classes = None
		self.max_length = None
		self.pattern = None
		self.inset_text_right = None
		self.inset_text_left = None
		self.icon_right = None
		self.icon_left = None

def get_form_field_input_type_by_type(type):
	from .models import FormField
	if type == FormField.TEXT_FIELD:
		return 'text'

	if type == FormField.EMAIL_FIELD:
		return 'email'

	if type == FormField.URL_FIELD:
		return 'url'

	if type == FormField.INTEGER_FIELD:
		return 'number'

	if type == FormField.NUMBER_FIELD:
		return 'number'

	if type == FormField.HIDDEN_FIELD:
		return 'hidden'

	if type == FormField.HONEYPOT_FIELD:
		return 'text'

	elif type == FormField.TEXT_AREA:
		return 'text' #TODO

	elif type == FormField.BOOLEAN_CHECKBOXES:
		return 'checkbox'

	elif type == FormField.BOOLEAN_TOGGLE:				
		return 'checkbox'

	elif type == FormField.SELECT_DROPDOWN:
		return 'select'

	elif type == FormField.SELECT_RADIO_BUTTONS:
		return 'radio'

	elif type == FormField.SELECT_BUTTONS:
		return 'radio'

	elif type == FormField.SELECT_IMAGE:
		return 'radio'

	elif type == FormField.SELECT_MULTIPLE_CHECKBOXES:
		return 'checkbox'

	elif type == FormField.SELECT_MULTIPLE_AUTOSUGGEST:
		return 'select' #TODO

	elif type == FormField.SELECT_MULTIPLE_HORIZONTAL:
		return 'select' #TODO

	elif type == FormField.SELECT_MULTIPLE_IMAGES:
		return 'checkbox'

	elif type == FormField.COMMA_SEPARATED_LIST:
		return 'text'
	
	elif type == FormField.FILE:
		return 'file'

	elif type == FormField.SECURE_FILE:
		return 'file'

	elif type == FormField.IMAGE:
		return 'file'

	elif type == FormField.DATE:
		return 'text'

	elif type == FormField.TIME:
		return 'text'

	elif type == FormField.DATE_TIME:
		return 'text'

	elif type == FormField.SCORE:
		return 'number'

	elif type == FormField.RANGE:
		return 'range'

	elif type == FormField.NUMBER_SLIDER:
		return 'number'

	elif type == FormField.PASSWORD:
		return 'password'

	return 'text'


def get_form_field_by_type(type, data, label='', choices=None):
	from .models import FormField
	"""
	data should provide:
	- is_required:Boolean
	- secondary_label
	- placeholder
	- help_text

	Optional:
	
	- icon:font awesome class
	- extra_css_classes: char
	- max_length
	- pattern
	- inset_text_right
	- inset_text_left
	- icon_right: font awesome
	- icon_left: font awesome
	"""

	field = None

	if type == FormField.TEXT_FIELD:
		field = forms.CharField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.EMAIL_FIELD:
		field = forms.EmailField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.URL_FIELD:
		field = forms.CharField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.INTEGER_FIELD:
		field = forms.IntegerField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.NUMBER_FIELD:
		field = forms.DecimalField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.TEXT_AREA:
		field = forms.CharField(widget=MultiLineText(model_field=data), label=label)

	elif type == FormField.BOOLEAN_CHECKBOXES:
		field = forms.BooleanField(widget=Checkbox(model_field=data), label=label)

	elif type == FormField.BOOLEAN_TOGGLE:				
		field = forms.BooleanField(widget=Checkbox(model_field=data), label=label)

	elif type == FormField.SELECT_DROPDOWN:
		field = forms.ChoiceField(widget=Select(model_field=data,choices=choices), label=label, choices=choices)

	elif type == FormField.SELECT_RADIO_BUTTONS:
		field = forms.ChoiceField(widget=Select(model_field=data,choices=choices), label=label, choices=choices)

	elif type == FormField.SELECT_BUTTONS:
		field = forms.ChoiceField(widget=Select(model_field=data,choices=choices), label=label, choices=choices)

	elif type == FormField.SELECT_IMAGE:
		field = forms.ChoiceField(widget=Select(model_field=data,choices=choices), label=label, choices=choices)

	elif type == FormField.SELECT_MULTIPLE_CHECKBOXES:
		field = MultipleChoiceField(widget=SelectMultiple(model_field=data), label=label, choices=choices)

	elif type == FormField.SELECT_MULTIPLE_AUTOSUGGEST:
		field = MultipleChoiceField(widget=SelectMultiple(model_field=data), label=label, choices=choices)

	elif type == FormField.SELECT_MULTIPLE_HORIZONTAL:
		field = MultipleChoiceField(widget=SelectMultiple(model_field=data), label=label, choices=choices)

	elif type == FormField.SELECT_MULTIPLE_BUTTONS:
		field = MultipleChoiceField(widget=SelectMultiple(model_field=data), label=label, choices=choices)

	elif type == FormField.SELECT_MULTIPLE_IMAGES:
		field = MultipleChoiceField(widget=SelectMultiple(model_field=data), label=label, choices=choices)

	elif type == FormField.COMMA_SEPARATED_LIST:
		field = forms.CharField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.FILE:
		field = forms.FileField(widget=ClearableFile(model_field=data), label=label)

	elif type == FormField.SECURE_FILE:
		field = forms.FileField(widget=ClearableFile(model_field=data), label=label)

	elif type == FormField.DATE:
		field = forms.DateField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.TIME:
		field = forms.TimeField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.DATE_TIME:
		field = forms.DateTimeField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.HIDDEN_FIELD:
		field = forms.CharField(widget=SingleLineText(model_field=data), label=label)

	elif type == FormField.HONEYPOT_FIELD:
		field = forms.CharField(widget=SingleLineText(model_field=data), label=label)
		
	else:
		#DEFAULT:
		field = forms.CharField(widget=SingleLineText(model_field=data), label=label)

	# is_required = models.BooleanField(default=False, 
	#     help_text=help['is_required'])    
	# is_digits = models.BooleanField(default=False, 
	#     help_text=help['is_digits'])
	# is_alphanumeric = models.BooleanField(default=False, 
	#     help_text=help['is_alphanumeric'])

	if field:

		field.required = data.is_required    


		field.secondary_label = '' if hasattr(data, 'secondary_label')==False else data.secondary_label
		field.placeholder_text = '' if hasattr(data, 'placeholder_text')==False else data.placeholder_text
		field.help_text = '' if hasattr(data, 'help_text')==False else data.help_text
		field.field_model = data

	
	return field