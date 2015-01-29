from django.conf import settings

from django.http import HttpResponse, Http404, HttpResponseRedirect, \
    HttpResponseForbidden, HttpResponsePermanentRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin
from django.template import loader, Context, RequestContext, Template
from django.template.response import SimpleTemplateResponse

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

    def render_to_response(self, context, **response_kwargs):
        if self.object.template:
            
            response_kwargs.setdefault('content_type', self.content_type)
            return CustomTemplateResponse(
                request=self.request,
                template=self.object.template,
                context=context,
                **response_kwargs
            )

        return super(AddressibleView, self).render_to_response(context)
        
        

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


class CustomTemplateResponse(SimpleTemplateResponse):
    rendering_attrs = SimpleTemplateResponse.rendering_attrs + ['_request', '_current_app']

    def __init__(self, request, template, context=None, content_type=None,
            status=None, current_app=None):

        self.template_object = template
        self._request = request
        self._current_app = current_app
        super(CustomTemplateResponse, self).__init__(
            template, context, content_type, status)

    @property
    def rendered_content(self):
        context = self.resolve_context(self.context_data)
        return self.template_object.render(context)

    def resolve_context(self, context):
        if isinstance(context, Context):
            return context
        return RequestContext(self._request, context, current_app=self._current_app)        