from django import forms
from ckeditorfiles.widgets import CKEditorWidget, CKEditorInlineWidget
from .models import *

class PageAdminForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['page_content_ckeditor']), required=False)
	synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['page_synopsis_ckeditor']), required=False)
	class Meta:
		model = Page
		fields = '__all__'


class PageContentBlockAdminForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorInlineWidget(config=settings.CKEDITOR_CONFIGS['pagecontentblock_content_ckeditor']), required=False)
	synopsis = forms.CharField(widget=CKEditorInlineWidget(config=settings.CKEDITOR_CONFIGS['pagecontentblock_synopsis_ckeditor']), required=False)
	
	class Meta:
		model = PageContentBlock
		fields = '__all__'

