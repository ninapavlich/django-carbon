from django import forms
from django.forms.widgets import HiddenInput
from django.utils.safestring import mark_safe

from django_ace import AceWidget

from .models import *


from carbon.compounds.form.utils import get_form_field_by_type, FieldData




class EmailTemplateAdminForm(forms.ModelForm):
    body_template = forms.CharField(widget=AceWidget(mode='html', width="850px", height="800px", showprintmargin=True), required=False)
    subject_template = forms.CharField(widget=AceWidget(mode='html', width="850px", height="200px", showprintmargin=True), required=False)
    
class EmailCategorySubscriptionSettingsForm(forms.Form):
	from carbon.compounds.form.models import FormField

	parent = forms.CharField(widget=HiddenInput())

	category = get_form_field_by_type(FormField.HIDDEN_FIELD, FieldData(is_required=True))
	status = get_form_field_by_type(FormField.SELECT_RADIO_BUTTONS, FieldData(is_required=True), 
		choices=EmailCategorySubscriptionSettings.NOTIFICATION_STATUS_CHOICES,
		label='Subscription Status')

	# print 'parent? %s'%(parent)
	# print 'category? %s'%(category)