from django.conf import settings

from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin


class PublishableView(SingleObjectMixin):


    def get_object(self, queryset=None):
        
        object = super(PublishableView, self).get_object(queryset)
        
        if self.object.is_published() == False:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': queryset.model._meta.verbose_name})

        return object  


class ModerationView(SingleObjectMixin):


    def get_object(self, queryset=None):
        
        object = super(ModerationView, self).get_object(queryset)
        
        if self.object.is_published() == False:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': queryset.model._meta.verbose_name})

        return object  


        