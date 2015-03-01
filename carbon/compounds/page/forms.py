from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='page_content_ckeditor'), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config_name='page_synopsis_ckeditor'), required=False)
    class Meta:
        model = Page


class UploadFileForm(forms.Form):
    file  = forms.FileField(required=True)
