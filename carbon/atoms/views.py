from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.translation import ugettext as _
from django.views.generic import DetailView

from .models import PageBase

class CategorizableListView(ListView):

    def get_queryset(self):
        queryset = self.model.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.published()
        return queryset


class CategorizableDetailView(DetailView):
    
   def get_context_data(self, **kwargs):
        ctx = super(CategorizableDetailView, self).get_context_data(**kwargs)
        #TODO: Add pagination to list if context is specified
       
        return ctx

class AddressibleListView(ListView):
    pass

class AddressibleDetailView(DetailView):
    pass

class PublishableListView(ListView):
    pass
    #return only items that are published

class PublishableDetailView(DetailView):
    pass
    #return only items that are published

class AccessibleListView(ListView):
    pass
    #return only items that are published

class AccessibleDetailView(DetailView):
    pass
    #return only items that are published


clss
    def render_to_response(self, context, **response_kwargs):
        #If page has special authentication:
        if self.object.authentication_required > 0:            
            if self.object.authentication_required >= Page.REGISTERED_USER and not self.request.user.is_authenticated():
                return HttpResponseRedirect( reverse("auth_login") )
            elif self.object.authentication_required >= Page.ADMIN and self.request.user.is_staff == False:
                return HttpResponseForbidden()
        
        #If page is a redirect page:
        if self.object.redirect_page == True:
            return HttpResponseRedirect( self.object.redirect_path )
            
        return super(PageDetail, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        """
        Returns the context for the PageDetail template
        """
        ctx = super(PageDetail, self).get_context_data(**kwargs)
        ctx.update({
            "children":self.object.get_published_children(),
            "current":self.object.slug
        })
       
        return ctx

    def get_template_names(self):
        names = super(PageDetail, self).get_template_names()
        if self.object and hasattr(self.object, "template_name"):
            name = getattr(self.object, "template_name")
            if name:
                names.insert(0, name)
        return names
