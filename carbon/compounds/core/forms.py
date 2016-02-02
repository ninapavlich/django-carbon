from django import forms
from django_ace import AceWidget
from ace_overlay.widgets import AceOverlayWidget
from django.utils.safestring import mark_safe
from .models import *


class TemplateAdminForm(forms.ModelForm):
    custom_template = forms.CharField(widget=AceOverlayWidget(mode='html', wordwrap=True, theme='github', width="850px", height="700px", showprintmargin=True), required=False)
    # class Meta:
    #     model = Template


class CSSResourceAdminForm(forms.ModelForm):
    custom_source = forms.CharField(widget=AceOverlayWidget(mode='sass', wordwrap=True, theme='github', width="850px", height="800px", showprintmargin=True), required=False)
    # class Meta:
    #     model = CSSResource   

class JSResourceAdminForm(forms.ModelForm):
    custom_source = forms.CharField(widget=AceOverlayWidget(mode='javascript', wordwrap=True, theme='github', width="850px", height="800px", showprintmargin=True), required=False)
    # class Meta:
    #     model = JSResource   


class UploadFileForm(forms.Form):
    file  = forms.FileField(required=True)
        
class MenuItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].help_text = mark_safe('To set this link to an existing\
        item in the cms, choose a Content Type and Object ID.')
        
        self.fields['path_override'].help_text = mark_safe('To set this link to an external \
        URL or absolute path, use the Path Override field.<br /><br />\
        External URLs should use this format "http://www.example.com" and absolute \
        URLs should use this format "/path/to/page/"') 