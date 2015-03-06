from django import forms
from ckeditorfiles.widgets import CKEditorWidget
from .models import *

class BlogArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogarticle_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogarticle_synopsis_ckeditor']), required=False)
    class Meta:
        model = BlogArticle

class BlogCategoryAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogcategory_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogcategory_synopsis_ckeditor']), required=False)
    class Meta:
        model = BlogCategory

class BlogTagAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogtag_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogtag_synopsis_ckeditor']), required=False)
    class Meta:
        model = BlogTag



