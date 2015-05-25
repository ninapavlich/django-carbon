import logging
try:
    from PIL import Image
except ImportError:
    import Image

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.db.models.loading import get_model
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.views.generic import DetailView, ListView

from carbon.atoms.views.abstract import *

from .models import *
from .forms import *


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
    
    def get(self, request, *args, **kwargs):

        self.object = self.get_object()      
        
        settings = self.object.get_settings()
        settings_data = [{'parent':item.parent.pk,'category':item.category.pk,'status':item.status} for item in settings]

        EmailCategorySubscriptionSettingsFormSet = formset_factory(EmailCategorySubscriptionSettingsForm, extra=0)
        self.formset = EmailCategorySubscriptionSettingsFormSet(initial=settings_data)
        
        context = self.get_context_data(object=self.object, formset=self.formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()  

        EmailCategorySubscriptionSettingsFormSet = formset_factory(EmailCategorySubscriptionSettingsForm, extra=0)
        self.formset = ArticleFormSet(request.POST, request.FILE)
        
        if self.forset.is_valid():        
            messages.success(request, 'Your subscription settings were updated')
        else:        
            messages.error(request, 'Please correct the errors below')

        context = self.get_context_data(object=self.object, formset=self.formset)
        return self.render_to_response(context)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)
    
class EmailRecordView( DetailView):
    slug_url_kwarg = 'access_key'
    slug_field = 'access_key'

    def render_to_response(self, context, **response_kwargs):  

        sites = Site.objects.all()
        from_any_internal_site = is_request_from_any_internal_site(self.request, sites)
        if from_any_internal_site == False:
            self.object.record_view()
        
        return output_spaceball_image()

def is_request_from_any_internal_site(request, sites):
    for site in sites:
        if request_originated_from_site(request, site) == True:
            return True
    return False

def is_request_from_any_online_view(request, sites, receipt):
    for site in sites:
        if request_originated_from_online_view(request, site, receipt) == True:
            return True
    return False    

def request_originated_from_site(request, site):
    if "HTTP_REFERER" in request.META:
        referer = request.META['HTTP_REFERER']
        if site.domain in referer:
            return True
    return False

def request_originated_from_online_view(request, site, receipt):
    if request_originated_from_site(request, site):
        online_url = receipt.get_rendered_url()
        referer = request.META['HTTP_REFERER']
        if online_url in referer:
            return True
    return False    

def output_spaceball_image():

    img = Image.new("RGB", (1,1), "#ffffff")
    response = HttpResponse(content_type="image/jpeg")
    img.save(response, "JPEG")
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