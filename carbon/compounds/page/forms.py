from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(), required=False)
    class Meta:
        model = Page


class UploadFileForm(forms.Form):
    file  = forms.FileField(required=True)
