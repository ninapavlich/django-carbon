from django.utils.encoding import force_text

from django.forms.utils import flatatt, to_current_timezone
from django.forms.widgets import TextInput as BaseTextInput
from django.forms.widgets import Textarea as BaseTextarea
from django.forms.widgets import CheckboxInput as BaseCheckboxInput
from django.forms.widgets import Select as BaseSelect


from django.template import loader
from django.template import Context, Template
from django.utils.html import conditional_escape, format_html


class BaseFormInput(object):
    has_custom_render = True
    model_field = None
    bound_field = None
    file_template = 'form/partials/base_field_container.html'

    def __init__(self, model_field, attrs=None):
        self.model_field = model_field
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

    def render_input(self, context_data, context=None):
        if context==None:
            context = Context(context_data)


        context['model_field'] = self.model_field
        context['field'] = self.bound_field

        

        # return DjangoTemplate(self.custom_template).render(final_attrs)
        template = loader.get_template(self.file_template)
        
        return template.render(context)


class TextInputWidget(BaseFormInput, BaseTextInput):
    input_type = 'text'


    def render(self, field, context=None, attrs=None):
        self.bound_field = field

        value = field.value()
        name = field.html_name
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))        
        
        return self.render_input(final_attrs, context)

class Textarea(BaseFormInput, BaseTextarea):

    def render(self, field, context=None, attrs=None):
        self.bound_field = field
        value = field.value()
        name = field.html_name

        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return self.render_input(final_attrs, context)

class CheckboxInput(BaseFormInput, BaseCheckboxInput):
    
    def check_test(self, v):
        return not (v is False or v is None or v == '')

    def render(self, field, context=None, attrs=None):
        self.bound_field = field
        value = field.value()
        name = field.html_name

        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return self.render_input(final_attrs, context)

class Select(BaseFormInput, BaseSelect):
    def render(self, field, context=None, attrs=None):
        self.bound_field = field
        value = field.value()
        name = field.html_name

        final_attrs = self.build_attrs(attrs, name=name)

        return self.render_input(final_attrs, context)

class MultiSelect(BaseFormInput, MultipleChoiceField):
    def render(self, field, context=None, attrs=None):
        self.bound_field = field
        value = field.value()
        name = field.html_name

        final_attrs = self.build_attrs(attrs, name=name)

        return self.render_input(final_attrs, context)