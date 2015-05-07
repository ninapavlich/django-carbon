from django import forms
from django.conf import settings

from ckeditorfiles.widgets import CKEditorInlineWidget
from .models import *

class FormFieldInlineAdminForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorInlineWidget(config=settings.CKEDITOR_CONFIGS['page_content_ckeditor']), required=False)
	
	class Meta:
		model = FormField
		fields = '__all__'


class FormEntryForm(forms.ModelForm):
	
	form_field_prefix = 'form_field_'

	class Meta:
		model = FormEntry
		fields = ['form']

	def __init__(self, form, *args, **kwargs):
		self.form = form
		super(FormEntryForm, self).__init__(*args, **kwargs)

		self.fields['form'].initial = self.form

		self.form_fields = form.get_input_fields()
		for field in self.form_fields:
			#TODO -- generate corresponding form field
			self.fields[self.form_field_prefix+field.slug] = field.get_widget()