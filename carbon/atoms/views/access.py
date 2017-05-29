from django.conf import settings

from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages

class BaseAccessView(SingleObjectMixin):

    access_login_template = None

    def is_request_authorized(self, request):
        return False

    def post(self, request, *args, **kwargs):

        self.object = super(BaseAccessView, self).get_object()
        if self.object.is_authorized(self.request) == False:
            if self.is_request_authorized(self.request):
                self.object.authorize_request(request)
                
        return super(BaseAccessView, self).post(request, *args, **kwargs)


    def get_template_names(self):
        self.object = super(BaseAccessView, self).get_object()
        if self.object.is_authorized(self.request) == False:
            return [self.access_login_template]
        return super(BaseAccessView, self).get_template_names()

class AccessKeyView(BaseAccessView):
    access_key_error_message = "Please enter a valid access key"
    def is_request_authorized(self, request):
        key = self.request.POST['access_key']
        is_key_valid =  self.object.test_key(key)
        if is_key_valid == False:
            messages.error(request, self.access_key_error_message)
        return is_key_valid
            
        

class AccessibleView(BaseAccessView):

    pass