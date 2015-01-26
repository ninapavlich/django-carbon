from django.views.generic import DetailView
from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *

from .templates import CustomTemplateResponse
#from django.template.response import TemplateResponse

class PageDetail(NonAdminCachableView, AddressibleView, PublishableView, DetailView):

    model = Page

    def render_to_response(self, context, **response_kwargs):
        if self.object.template:
            response_kwargs.setdefault('content_type', self.content_type)
            return CustomTemplateResponse(
                request=self.request,
                template=self.object.template,
                context=context,
                **response_kwargs
            )

        return super(PageDetail, self).render_to_response(context)

