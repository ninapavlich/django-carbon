from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse

# from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
# from extra_views.generic import GenericInlineFormSet


from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.template import loader, Context, RequestContext, Template
from django.template.response import SimpleTemplateResponse

from carbon.atoms.views.abstract import *


# class FieldEntryInline(GenericInlineFormSet):
#     # model = FieldEntry
#     pass


# class CreateFormEntryView(CreateWithInlinesView):
#     # model = FormEntry
#     inlines = [FieldEntryInline]

class FormSubmittedView(AddressibleView, DetailView):
	
	def get_template(self):
		return self.object.submit_template

	

class CreateFormEntryView(AddressibleView, FormMixin, ProcessFormView):
	content_type = None
	def get_form_kwargs(self):

		#ADD REFERNCE TO FORM OBJECT
		kwargs = super(CreateFormEntryView, self).get_form_kwargs()
		kwargs['form'] = self.object
		return kwargs

	def get_success_url(self):
		return self.object.get_success_url()

	def form_valid(self, form):
		
		self.form_entry_object = form.save()
		
		self.object.handle_successful_submission(form, self.form_entry_object)
		return super(CreateFormEntryView, self).form_valid(form)


	# def form_invalid(self, form):
	# 	print "FORM INVALID!"
	# 	print "How many errors? %s"%(len(form.errors))
	# 	return self.render_to_response(self.get_context_data(form=form))

# class UpdateFormEntryView(UpdateWithInlinesView):
#     # model = FormEntry
#     inlines = [FieldEntryInline]