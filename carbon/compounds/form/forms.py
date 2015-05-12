from django import forms
from django.conf import settings


from ckeditorfiles.widgets import CKEditorInlineWidget
from ckeditorfiles.widgets import CKEditorWidget
from .models import *

class FormFieldInlineAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorInlineWidget(config=settings.CKEDITOR_CONFIGS['page_content_ckeditor']), required=False)
    
    # IMPLEMENT
    # class Meta:
    #     model = FormField
    #     fields = '__all__'


class FormAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['page_content_ckeditor']), required=False)
    submission_content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['page_content_ckeditor']), required=False)
    
    class Meta:
        # model = Form
        fields = '__all__'


class FormEntryForm(forms.ModelForm):
    
    form_field_prefix = 'form_field_'
    form_fields = []

    # IMPLEMENT
    # field_model = FieldEntry
    # class Meta:
    #     model = FormEntry
    #     fields = ['form']

    def __init__(self, form_schema, *args, **kwargs):
        self.form_schema = form_schema
        super(FormEntryForm, self).__init__(*args, **kwargs)

        self.fields['form_schema'].initial = self.form_schema

        self.model_form_fields = self.form_schema.get_all_fields()
        
        for model_field in self.model_form_fields:
            form_field = model_field.get_form_field()
            key = self.form_field_prefix+model_field.slug
            self.fields[key] = form_field
            self.form_fields.append(form_field)

    

    def get_form_fields(self):
        return self.form_fields

    def save(self, **kwargs):
        entry = super(FormEntryForm, self).save()
        
        # entry.record_entry(self)
        for field_key in self.fields:
            if self.form_field_prefix in field_key:
                field = self.fields[field_key]
                value = self._raw_value(field_key)
                
                
                field_entry, created = self.field_model.objects.get_or_create(form_entry=entry, form_field=field.widget.model_field)
                # if created:
                #     print 'created new field entry: %s, %s, %s'%(field_entry, entry.pk, field.widget.model_field.title)
                # else:
                #     print 'Update field entry %s'%(value)
                field_entry.value = field_entry.get_compressed_value(value)
                field_entry.save()
        

        return entry