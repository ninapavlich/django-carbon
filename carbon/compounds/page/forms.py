from django import forms
from ckeditor.widgets import CKEditorWidget
from django_ace import AceWidget
from .models import *

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Page


class TemplateAdminForm(forms.ModelForm):
    custom_template = forms.CharField(widget=AceWidget(mode='html', width="850px", height="800px", showprintmargin=True), required=False)
    class Meta:
        model = Template


    