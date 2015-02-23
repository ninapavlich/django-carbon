from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class BlogArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)
    class Meta:
        model = BlogArticle
