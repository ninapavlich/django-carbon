from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
import django.dispatch
from django.http import QueryDict

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.template import loader, Context, RequestContext, Template
from django.template.response import SimpleTemplateResponse

from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *


signal_form_error = django.dispatch.Signal(providing_args=["form_schema"])
signal_form_entry_created = django.dispatch.Signal(providing_args=["form_schema", "form_entry"])
signal_form_entry_updated = django.dispatch.Signal(providing_args=["form_schema", "form_entry"])


class FormSignalOperator(FormMixin, ProcessFormView):
    default_error_message = "Please correct the errors below."
    default_success_message = "Your form was saved."

    def get_form_schema(self):
        raise ImproperlyConfigured("View should override get_form_schema() function")

    def get_form_schema(self):
        raise ImproperlyConfigured("View should override get_form_schema() function")

    def get_is_create_form(self):
        raise ImproperlyConfigured("View should override get_is_create_form() function")

    def form_invalid(self, form):
        form_schema = self.get_form_schema()
        if form_schema:
            messages.error(self.request, form_schema.form_error_message or self.default_error_message)
            form_schema_class = type(form_schema)
            signal_form_error.send(sender=form_schema_class, form_schema=form_schema)
        else:
            messages.error(self.request, self.default_error_message)

        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        self.form_entry_object = form.save()
        created = self.get_is_create_form()

        form_schema = self.get_form_schema()
        if form_schema:
            messages.success(self.request, form_schema.form_create_message or self.default_success_message)        
            form_schema.handle_successful_submission(form, self.form_entry_object, created)

            form_entry_class = type(self.form_entry_object)
            if created:
                signal_form_entry_created.send(sender=form_entry_class, form_schema=form_schema, form_entry=self.form_entry_object)
            else:
                signal_form_entry_updated.send(sender=form_entry_class, form_schema=form_schema, form_entry=self.form_entry_object)

        return super(FormSignalOperator, self).form_valid(form)



class FormSubmittedView(AddressibleView, PublishableView, DetailView):
    
    def get_template_names(self):

        return [self.object.submit_template.slug]

    

class CreateFormEntryMixin(FormSignalOperator):
    content_type = None
    form_entry_object = None
    default_success_message = "Your form was created."

    def get_form_schema(self):
        #Override in subclass
        raise ImproperlyConfigured("View should override get_form_schema() function")

    def get_is_create_form(self):
        return True

    def get(self, request, *args, **kwargs):
        self.form_schema = self.get_form_schema()
        if self.form_schema:
            self.form = form = self.get_form()
        return super(CreateFormEntryMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_schema = self.get_form_schema()
        if self.form_schema:
            self.form = form = self.get_form()
        
        return super(CreateFormEntryMixin, self).post(request, *args, **kwargs)
    

    def get_form_kwargs(self):      
        #ADD REFERNCE TO FORM OBJECT
        kwargs = super(CreateFormEntryMixin, self).get_form_kwargs()
        kwargs['form_schema'] = self.form_schema
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return self.form_schema.get_success_url(self.form_entry_object)


    def get_context_data(self, **kwargs):
        context = super(CreateFormEntryMixin, self).get_context_data(**kwargs)
        context['form'] = None
        context['has_form'] = False
        context['form_entry_object'] = self.form_entry_object
        context['form_schema'] = self.form_schema

        if hasattr(self, 'form'):
            context['has_form'] = True
            context['form'] = self.form
        return context


class CreateFormEntryView(AddressibleView, PublishableView, FormSignalOperator):
    content_type = None
    form_entry_object = None
    default_success_message = "Your form was created."

    def get_form_kwargs(self):
        
        #ADD REFERNCE TO FORM OBJECT
        kwargs = super(CreateFormEntryView, self).get_form_kwargs()
        kwargs['form_schema'] = self.object
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return self.object.get_success_url(self.form_entry_object)

    def get_form_schema(self):
        return self.object

    def get_is_create_form(self):
        return True


    def get_context_data(self, **kwargs):
        context = super(CreateFormEntryView, self).get_context_data(**kwargs)
        context['form_entry_object'] = self.form_entry_object
        return context


class UpdateFormEntryView(PublishableView, AddressibleView, FormSignalOperator):
    content_type = None
    form_entry_object = None
    form_entry_class = None
    default_success_message = "Your form was updated."

    def get_form_kwargs(self):
        
        kwargs = super(UpdateFormEntryView, self).get_form_kwargs()

        #ADD REFERNCE TO FORM OBJECT AND FIELD DATA
        kwargs['form_schema'] = self.object
        kwargs['request'] = self.request
        kwargs['instance'] = self.form_entry_object
        

        if self.request.method in ('POST', 'PUT'):
            
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
            
        else:
            
            data = {'form_schema':self.object.pk}
            fields = self.form_entry_object.get_entries()
            for field in fields:
                key = self.form_class.form_field_prefix+field.form_field.slug
                data[key] = field.decompressed_value

            qdict = QueryDict('', mutable=True)
            qdict.update(data)
            kwargs['data'] = qdict

        

        return kwargs

    def get(self, request, *args, **kwargs):
        self.form_entry_object = self.get_form_entry()
        return super(UpdateFormEntryView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form_entry_object = self.get_form_entry()
        return super(UpdateFormEntryView, self).post(request, *args, **kwargs)

    def get_form_entry(self):
        if self.form_entry_object:
            return self.form_entry_object

        pk = self.kwargs.get('pk', '')

        queryset = self.form_entry_class._default_manager.all()
        try:
            obj = queryset.filter(pk=pk)[0]
        except:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': queryset.model._meta.verbose_name})
        return obj


    def get_success_url(self):
        return self.object.get_success_url(self.form_entry_object)

    def get_form_schema(self):
        return self.form_entry_object.form_schema

    def get_is_create_form(self):
        return False


    def get_context_data(self, **kwargs):
        context = super(UpdateFormEntryView, self).get_context_data(**kwargs)
        context['form_entry_object'] = self.form_entry_object
        return context