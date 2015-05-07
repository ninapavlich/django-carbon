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
	form_fields = []

	class Meta:
		model = FormEntry
		fields = ['form']

	def __init__(self, form, *args, **kwargs):
		self.form = form
		super(FormEntryForm, self).__init__(*args, **kwargs)

		self.fields['form'].initial = self.form

		self.model_form_fields = form.get_input_fields()
		for model_field in self.model_form_fields:

			form_field = model_field.get_form_field()
			key = self.form_field_prefix+model_field.slug
			self.fields[key] = form_field
			self.form_fields.append(form_field)

	def get_form_fields(self):
		return self.form_fields