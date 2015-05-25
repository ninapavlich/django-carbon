import logging
try:
    from PIL import Image
except ImportError:
    import Image

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models.loading import get_model
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic import DetailView, ListView
from django.db.models.loading import get_model

from carbon.atoms.views.abstract import *

from .models import *


class EmailOnlineView(CustomResponseView, DetailView):
    slug_url_kwarg = 'access_key'
    slug_field = 'access_key'

class EmailRenderedView(DetailView):
    slug_url_kwarg = 'access_key'
    slug_field = 'access_key'

    def render_to_response(self, context, **response_kwargs):
            
        return HttpResponse(self.object.rendered_body, content_type="text/html")


class EmailSettingsView(CustomResponseView, DetailView):
    slug_url_kwarg = 'access_key'
    slug_field = 'access_key'
    
    
class EmailRecordView(CustomResponseView, DetailView):
    slug_url_kwarg = 'access_key'
    slug_field = 'access_key'
    pass



def output_receipt_image():

    img = Image.new("RGB", (1,1), "#ffffff")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


#Detail view
def record_email_view(request, key):
    site = Site.objects.get_current()        

    if "HTTP_REFERER" in request.META and site.domain in request.META['HTTP_REFERER']:
        #dont track if image is embedded on server
        pass
    else:
        
        if key:
            try:
                email_receipt_model = get_model_by_label(settings.EMAIL_RECEIPT_MODEL)
                receipt = email_receipt_model.objects.get(key=key)
            except:
                receipt = None

            if receipt:
                receipt.record_view()

    return output_receipt_image()


#Detail view
def email_receipt_view(request, pk):

    if request.user and request.user.is_authenticated() and request.user.is_staff:

        if pk:
            try:
                receipt = EmailReceipt.objects.get(pk=pk)
            except:
                receipt = None

            if receipt:
                return HttpResponse(receipt.rendered_body, content_type="application/xhtml+xml")

    return HttpResponseForbidden()    


def get_model_by_label(label):
    app_label = label.split('.')[0]
    object_name = label.split('.')[1]
    return get_model(app_label, object_name)    