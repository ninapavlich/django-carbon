from django import forms
from django_ace import AceWidget
from django.utils.safestring import mark_safe
from .models import *


class EmailTemplateAdminForm(forms.ModelForm):
    body_template = forms.CharField(widget=AceWidget(mode='html', width="850px", height="800px", showprintmargin=True), required=False)
    subject_template = forms.CharField(widget=AceWidget(mode='html', width="850px", height="200px", showprintmargin=True), required=False)
    
