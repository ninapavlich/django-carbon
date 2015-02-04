from django import forms
from django_ace import AceWidget
from .models import *


class TemplateAdminForm(forms.ModelForm):
    custom_template = forms.CharField(widget=AceWidget(mode='html', width="850px", height="800px", showprintmargin=True), required=False)
    class Meta:
        model = Template