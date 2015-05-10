from django.conf import settings
from django.core.urlresolvers import reverse

# from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
# from extra_views.generic import GenericInlineFormSet


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

class CreateFormEntryView(AddressibleView, FormMixin, ProcessFormView):
	content_type = None
	def get_form_kwargs(self):

		#ADD REFERNCE TO FORM OBJECT
		kwargs = super(CreateFormEntryView, self).get_form_kwargs()
		kwargs['form'] = self.object
		return kwargs

	# def form_invalid(self, form):
	# 	print "FORM INVALID!"
	# 	print "How many errors? %s"%(len(form.errors))
	# 	return self.render_to_response(self.get_context_data(form=form))

# class UpdateFormEntryView(UpdateWithInlinesView):
#     # model = FormEntry
#     inlines = [FieldEntryInline]