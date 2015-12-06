from django.contrib import messages
from django.dispatch import receiver
from django.http import Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView

from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *
from carbon.compounds.form.views import signal_form_error, signal_form_entry_created


from .models import *
from .forms import *
from inertia.apps.form.models import Form, FormEntry
from inertia.utils.zoho import handle_form_entry

class PageDetail(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

	# model = Page
	pass


class SiblingPageDetail(NonAdminCachableView, PublishableView, AddressibleView, HasSiblingsView, DetailView):

	# model = Page
	pass	
	




class PageTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

	# model = PageTag
	pass

		
class PageBlockView(object):

	def get_context_data(self, **kwargs):
		
		ctx = super(PageBlockView, self).get_context_data(**kwargs)

		#PAGE CONTENT BLOCKS
		pageblocks = self.get_page_content_blocks()
		for pageblock in pageblocks:
			ctx[pageblock.slug] = pageblock

		ctx['page_blocks'] = pageblocks
	   
		return ctx

	def get_page_content_blocks(self):

		return self.object.get_page_content_blocks()


@receiver(signal_form_error, sender=Form)
def on_form_error(sender, **kwargs):
	form = kwargs['form_schema']
    #pass...

@receiver(signal_form_entry_created, sender=FormEntry)
def on_form_created(sender, **kwargs):
    form_entry = kwargs['form_entry']
    handle_form_entry(form_entry)