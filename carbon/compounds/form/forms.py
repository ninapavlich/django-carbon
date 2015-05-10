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


    # def is_valid(self):
    #   form_errors = self.errors
    #   print "ENTRY FORM ERRORS: %s"%(form_errors)
    #   return self.is_bound and not bool(form_errors)

    # def full_clean(self):
    #   print 'self.is_bound? %s'%(self.is_bound)
    #   return super(FormEntryForm, self).full_clean()

    # def _clean_fields(self):
    #   print 'clean fields.'
    #   print 'self.is_bound? %s'%(self.is_bound)
    #   for name, field in self.fields.items():
    #       print "NAME? %s Field? %s"%(name, field)

    #   super(FormEntryForm, self)._clean_fields()

    def __init__(self, form, *args, **kwargs):
        self.form = form
        print "INIT FORM!"
        super(FormEntryForm, self).__init__(*args, **kwargs)

        self.fields['form'].initial = self.form

        self.model_form_fields = form.get_input_fields()
        # print 'MODELF FORM FIELDS? %s'%(self.model_form_fields)
        for model_field in self.model_form_fields:
            # print 'model field'
            # print model_field
            form_field = model_field.get_form_field()
            key = self.form_field_prefix+model_field.slug
            self.fields[key] = form_field
            self.form_fields.append(form_field)

            # print 'field %s - %s - %s'%(key, form_field, form_field.widget.model_field)

    def get_form_fields(self):
        return self.form_fields

    def save(self, **kwargs):
        entry = super(FormEntryForm, self).save()
        print 'CREATED NEW ENTRY: %s'%(entry.pk )

        # entry.record_entry(self)
        for field_key in self.fields:
            if self.form_field_prefix in field_key:
                field = self.fields[field_key]
                value = self._raw_value(field_key)
                print 'FIELD? %s model? %s value? %s'%(field, field.widget.model_field, value)

                

                field_entry, created = self.field_model.objects.get_or_create(form_entry=entry, form_field=field.widget.model_field)
                if created:
                    print 'created new field entry: %s'%(field_entry)
                    field_entry.value = value
                    field_entry.save()
        

        return entry