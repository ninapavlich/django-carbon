from os.path import join, split

from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage, DefaultStorage
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.utils.html import escape
from django.utils.module_loading import import_string


from ckeditorfiles.widgets import CKEditorInlineWidget
from ckeditorfiles.widgets import CKEditorWidget

from carbon.atoms.models.media import BaseSecureAtom
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
    auto_populate_get_values = True #Auto-populate values from GET into the forms initial values

    # IMPLEMENT
    # field_model = FieldEntry
    # class Meta:
    #     model = FormEntry
    #     fields = ['form']

    def __init__(self, form_schema, request, *args, **kwargs):
        self.form_schema = form_schema
        self.request = request
        super(FormEntryForm, self).__init__(*args, **kwargs)

        self.fields['form_schema'].initial = self.form_schema

        if self.form_schema:
            self.model_form_fields = self.form_schema.get_all_fields()
            
            for model_field in self.model_form_fields:
                form_field = model_field.get_form_field()
                key = self.form_field_prefix+model_field.slug
                self.fields[key] = form_field
                self.form_fields.append(form_field)


            #Auto-populate form fields with get values if applicable
            is_get = self.request.method=="GET"
            if is_get and self.auto_populate_get_values:
                for key in self.request.GET:
                    has_corresponding_form_field = key in self.fields
                    if has_corresponding_form_field:
                        self.fields[key].initial = self.request.GET[key]

        
        

    

    def get_form_fields(self):
        return self.form_fields

    def cleaned_value(self, value):
        value = escape(value)
        return value

    def _clean_fields(self):
        
        super(FormEntryForm, self)._clean_fields()

        for field_key in self.fields:
            if self.form_field_prefix in field_key:
                field = self.fields[field_key]
                raw_value = self._raw_value(field_key)
            
                try:
                    field.widget.model_field.validate(raw_value, self)
                except ValidationError as e:
                    self.add_error(field_key, e)



    def save(self, **kwargs):
        entry = super(FormEntryForm, self).save()
        
        # entry.record_entry(self)
        for field_key in self.fields:
            if self.form_field_prefix in field_key:
                field = self.fields[field_key]
                raw_value = self._raw_value(field_key)
                value = self.cleaned_value(raw_value)
                model_field = field.widget.model_field

                #TODO-- add secure file handling...
                if value and field.widget.model_field.is_multipart:

                    type = raw_value.__class__.__name__
                    # print 'TYPE? %s'%(type)
                    if isinstance(raw_value, InMemoryUploadedFile) or isinstance(raw_value, TemporaryUploadedFile):
                        
                        
                        file_upload_path = join('form_uploads', str(self.form_schema.slug), str(entry.pk), str(model_field.slug), raw_value.name)
                            # if settings.DEBUG:
                            #     print 'FILE UPLOAD PATH: %s'%(file_upload_path)
                        try:
                            
                            if model_field.type == FormField.SECURE_FILE:
                                
                                secure_file_storage = import_by_path(settings.SECURE_MEDIA_STORAGE)()
                                value = secure_file_storage.save(file_upload_path, raw_value)

                                key_name = "%s/%s"%(settings.AWS_MEDIA_FOLDER, value)
                                BaseSecureAtom.make_private(settings.AWS_STORAGE_BUCKET_NAME_MEDIA_SECURE, key_name)

                            else:
                                
                                file_storage = DefaultStorage()
                                value = file_storage.save(file_upload_path, raw_value)
                        except:
                            print "Error uploading file to %s/%s"%(file_upload_path, raw_value)
                            value = file_upload_path
                
                
                field_entry, created = self.field_model.objects.get_or_create(form_entry=entry, form_field=field.widget.model_field)
                # if created:
                #     print 'created new field entry: %s, %s, %s'%(field_entry, entry.pk, field.widget.model_field.title)
                # else:
                #     print 'Update field entry %s'%(value)
                field_entry.value = field_entry.get_compressed_value(value)
                field_entry.save()
        

        return entry