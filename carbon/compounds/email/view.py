import logging
try:
    from PIL import Image
except ImportError:
    import Image

from django.conf import settings
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.sites.models import Site

from .models import *


def output_receipt_image():

    img = Image.new("RGB", (1,1), "#ffffff")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def record_email_view(request, key):
    site = Site.objects.get_current()        

    if "HTTP_REFERER" in request.META and site.domain in request.META['HTTP_REFERER']:
        #dont track if image is embedded on server
        pass
    else:
        
        if key:
            try:
                receipt = EmailReceipt.objects.get(key=key)
            except:
                receipt = None

            if receipt:
                receipt.record_view()

    return output_receipt_image()

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