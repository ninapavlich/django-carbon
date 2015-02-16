from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _

from grappelli.views.related import AutocompleteLookup

#ADMIN VIEWS 








def clear_cache(request):
    
    if not request.user or not request.user.is_staff:
        raise Http404()

    try:
        cache.clear()
        messages.success(request, 'The cache has been cleared.')
    except:
        messages.warning(request, 'There was an error while attempting to clear the cache.')

    return redirect('admin:index')


class FilteredAutocomplete(AutocompleteLookup):
    """ patch grappelli's autocomplete to let us control the queryset 
    by creating a autocomplete_queryset function on the model """
    def get_queryset(self):
        if hasattr(self.model, "autocomplete_queryset"):
            qs = self.model.autocomplete_queryset()
        else:
            qs = self.model._default_manager.all()
        qs = self.get_filtered_queryset(qs)
        qs = self.get_searched_queryset(qs)
        return qs.distinct()    