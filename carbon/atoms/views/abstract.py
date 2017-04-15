from django.conf import settings

from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, Http404, HttpResponseRedirect, \
    HttpResponseForbidden, HttpResponsePermanentRedirect
from django.template import loader, Context, RequestContext, Template
from django.template.response import SimpleTemplateResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model



from .decorators import admins_skip_cache, users_skip_cache

from carbon.utils.template import get_template_by_pk_or_slug

class NonAdminCachableView(object):

    @method_decorator(admins_skip_cache)
    def dispatch(self, *args, **kwargs):
        return super(NonAdminCachableView, self).dispatch(*args, **kwargs)

class NonUserCachableView(object):

    @method_decorator(users_skip_cache)
    def dispatch(self, *args, **kwargs):
        return super(NonUserCachableView, self).dispatch(*args, **kwargs) 


class ObjectTemplateResponseMixin(object):

    template_name = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None
    
    def get_template_names(self):

        if self.object and self.object.template:
            return [self.object.template.slug]

        elif self.model and self.model.default_template:
            return [self.model.default_template]

        elif self.template_name is None:
            raise ImproperlyConfigured(
                "ObjectTemplateResponseMixin requires either a definition of "
                "'template_name' or an object with a .template instance'")
        else:
            return [self.template_name]

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        template_names = self.get_template_names()
        return self.response_class(
            request=self.request,
            template=template_names,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(ObjectTemplateResponseMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'object') and self.object != None:
            context['object_verbose_name'] = self.object._meta.verbose_name
            context['object_verbose_name_plural'] = self.object._meta.verbose_name_plural
            

        return context


# class CustomTemplateResponseMixin(object):

#   def get_template_names(self):
#       if not self.template_slug:
#           raise ImproperlyConfigured( "template_slug not defined.")
        
#       return [self.template_slug]


class HasSiblingsView(object):

    def get_siblings(self):
        
        try:
            return self.object.get_siblings()
        except:
            return None

    def get_next_previous(self, siblings):
        return (self.object.get_next_sibling(siblings), self.object.get_previous_sibling(siblings))

    def get(self, request, *args, **kwargs):
        self.siblings = self.get_siblings()
        self.next, self.previous = self.get_next_previous(self.siblings)

        return super(HasSiblingsView, self).get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):

        self.siblings = self.get_siblings()
        self.next, self.previous = self.get_next_previous(self.siblings)

        return super(HasSiblingsView, self).post(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super(HasSiblingsView, self).get_context_data(**kwargs)
        if self.siblings != None:
            context['siblings'] = self.siblings
            context['next'] = self.next
            context['previous'] = self.previous

        return context


class HasChildrenView(HasSiblingsView):
    paginate_by = 10
    paginate_orphans = 0
    paginator_class = Paginator
    allow_empty = True
    page_kwarg = 'page'

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.paginate_orphans,
            allow_empty_first_page=self.allow_empty)
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginator(self, queryset, per_page, orphans=0,
                        allow_empty_first_page=True, **kwargs):
        """
        Return an instance of the paginator for this view.
        """
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_children(self):
        try:
            return self.object.get_children()
        except:
            return None

    def get(self, request, *args, **kwargs):

        if not self.object:
            self.object = self.get_object()

        try:
            children = self.get_children()
            self.object_list = children
            self.children = children
        except:
             self.object_list = None 

        return super(HasChildrenView, self).get(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):

        if not self.object:
            self.object = self.get_object()

        try:
            children = self.get_children()
            self.object_list = children
            self.children = children
        except:
             self.object_list = None 


        return super(HasChildrenView, self).post(request, *args, **kwargs)


    


        

    def get_context_data(self, **kwargs):
        context = super(HasChildrenView, self).get_context_data(**kwargs)
        if self.object_list != None:
            paginator, page, queryset, is_paginated = self.paginate_queryset(self.object_list, self.paginate_by)
            context['paginator'] = paginator
            context['page_obj'] = page
            context['is_paginated'] = is_paginated
            context['object_list'] = queryset
            context['children'] = self.children
            context['siblings'] = self.siblings
            context['next'] = self.next
            context['previous'] = self.previous

        return context



class AddressibleView(ObjectTemplateResponseMixin, SingleObjectMixin):
    object = None
    catch_404s = True
    

    def get_template(self):
        print "TEMPLATE?? %s"%(self.object.template)
        return self.object.template

    def handle(self, request):

        if not self.object:
            self.object = self.get_object()

        if self.object.temporary_redirect != None and self.object.temporary_redirect != '':
            return HttpResponseRedirect( self.object.temporary_redirect )

        if self.object.permanent_redirect != None and self.object.permanent_redirect != '':
            return HttpResponsePermanentRedirect( self.object.permanent_redirect )

    def post(self, request, *args, **kwargs):

        self.handle(request)

        return super(AddressibleView, self).post(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        
        self.handle(request)

        return super(AddressibleView, self).get(request, *args, **kwargs)


    def get_object_query(self, queryset, path):
        return queryset.filter(path=path).select_related('template').get()

    def get_query_path(self):
        if self.kwargs.get('path'):
            path = self.kwargs.get('path', '')
        else:
            path = self.request.path

        #Make sure path starts and ends with slashes
        if not path.endswith("/"):
            path = "%s/"%path

        if not path.startswith("/"):
            path = "/%s"%path

        return path


    def get_object(self, queryset=None):
        
        if self.object:
            return self.object

        path = self.get_query_path()

        queryset = self.get_queryset()
        
        # search_path = path
        # if hasattr(self.model, 'url_domain') and self.model.url_domain:
        #     search_path = path.replace(self.model.url_domain, '')

        try:
            # print path
            # print queryset
            obj = self.get_object_query(queryset, path)
            return obj 
        except:
            if self.catch_404s:
                raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})

            return None