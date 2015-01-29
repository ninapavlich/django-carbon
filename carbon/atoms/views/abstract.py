from django.conf import settings

from django.http import HttpResponse, Http404, HttpResponseRedirect, \
    HttpResponseForbidden, HttpResponsePermanentRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin
from django.template import loader, Context

from .decorators import admins_skip_cache, users_skip_cache


class NonAdminCachableView(object):

    @method_decorator(admins_skip_cache)
    def dispatch(self, *args, **kwargs):
        return super(NonAdminCachableView, self).dispatch(*args, **kwargs)

class NonUserCachableView(object):

    @method_decorator(users_skip_cache)
    def dispatch(self, *args, **kwargs):
        return super(NonUserCachableView, self).dispatch(*args, **kwargs)    


class AddressibleView(SingleObjectMixin):
    object = None


    def post(self, request, *args, **kwargs):

        if not self.object:
            self.object = self.get_object()

        if self.object.temporary_redirect != None and self.object.temporary_redirect != '':
            return HttpResponseRedirect( self.object.temporary_redirect )

        if self.object.permanent_redirect != None and self.object.permanent_redirect != '':
            return HttpResponsePermanentRedirect( self.object.permanent_redirect )

        return super(AddressibleView, self).post(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        
        if not self.object:
            self.object = self.get_object()

        if self.object.temporary_redirect != None and self.object.temporary_redirect != '':
            return HttpResponseRedirect( self.object.temporary_redirect )

        if self.object.permanent_redirect != None and self.object.permanent_redirect != '':
            return HttpResponsePermanentRedirect( self.object.permanent_redirect )

        return super(AddressibleView, self).get(request, *args, **kwargs)
        
        

    def get_object(self, queryset=None):
        
        if self.object:
            return self.object

        if self.kwargs.get('path'):
            path = self.kwargs.get('path', '')
        else:
            path = self.request.path

        #Make sure path starts and ends with slashes
        if not path.endswith("/"):
            path = "%s/"%path

        if not path.startswith("/"):
            path = "/%s"%path

        queryset = self.get_queryset()
        
        try:
            obj = queryset.filter(path=path)[0]

        except:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': queryset.model._meta.verbose_name})

        return obj