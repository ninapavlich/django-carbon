from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *

class BlogArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='blogarticle_content_ckeditor'), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config_name='blogarticle_synopsis_ckeditor'), required=False)
    class Meta:
        model = BlogArticle

class BlogCategoryAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='blogcategory_content_ckeditor'), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config_name='blogcategory_synopsis_ckeditor'), required=False)
    class Meta:
        model = BlogCategory

class BlogTagAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='blogtag_content_ckeditor'), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config_name='blogtag_synopsis_ckeditor'), required=False)
    class Meta:
        model = BlogTag



