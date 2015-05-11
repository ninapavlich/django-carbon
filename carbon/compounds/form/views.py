from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import QueryDict

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.template import loader, Context, RequestContext, Template
from django.template.response import SimpleTemplateResponse

from carbon.atoms.views.abstract import *



class FormSubmittedView(AddressibleView, DetailView):
	
	def get_template(self):
		return self.object.submit_template

	

class CreateFormEntryView(AddressibleView, FormMixin, ProcessFormView):
	content_type = None
	form_entry_object = None

	def get_form_kwargs(self):
		
		#ADD REFERNCE TO FORM OBJECT
		kwargs = super(CreateFormEntryView, self).get_form_kwargs()
		kwargs['form_schema'] = self.object
		return kwargs

	def get_success_url(self):
		return self.object.get_success_url(self.form_entry_object)

	def form_valid(self, form):
		self.form_entry_object = form.save()		
		self.object.handle_successful_submission(form, self.form_entry_object, True)
		return super(CreateFormEntryView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateFormEntryView, self).get_context_data(**kwargs)
		context['form_entry_object'] = self.form_entry_object
		return context


class UpdateFormEntryView(AddressibleView, FormMixin, ProcessFormView):
	content_type = None
	form_entry_object = None
	form_entry_class = None

	def get_form_kwargs(self):
		
		kwargs = super(UpdateFormEntryView, self).get_form_kwargs()

		#ADD REFERNCE TO FORM OBJECT AND FIELD DATA
		kwargs['form_schema'] = self.object
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

	def form_valid(self, form):
		self.form_entry_object = form.save()		
		self.object.handle_successful_submission(form, self.form_entry_object, False)
		return super(UpdateFormEntryView, self).form_valid(form)		

	def get_context_data(self, **kwargs):
		context = super(UpdateFormEntryView, self).get_context_data(**kwargs)
		context['form_entry_object'] = self.form_entry_object
		return context