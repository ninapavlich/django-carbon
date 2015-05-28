from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.base import RedirectView

from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *
from .forms import *


class PageDetail(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

	# model = Page
	pass
	




class PageTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

	# model = PageTag
	pass

		
class PageBlockView(object):

	def get_context_data(self, **kwargs):
		
		print 'GET PAGE BLOCK CONTEXT!'
		ctx = super(PageBlockView, self).get_context_data(**kwargs)

		#PAGE CONTENT BLOCKS
		pageblocks = self.get_page_content_blocks()
		for pageblock in pageblocks:
			ctx[pageblock.slug] = pageblock

		ctx['page_blocks'] = pageblocks
	   
		return ctx

	def get_page_content_blocks(self):

		return self.object.get_page_content_blocks()
