from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.base import RedirectView

from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *
from .forms import *


class PageDetail(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    # model = Page
    pass
    



class PageTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = PageTag
    pass

        

def admin_import_links( request ):    
    

    if not request.user or not request.user.is_staff:
        raise Http404()

    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        import_file = request.FILES.get('file', None)

        if import_file:
            results = LegacyURL.import_links(import_file, request)

            messages.success(request, results)

        else:
            messages.warning(request, 'No .CSV file specified')
       
    else:
        form = UploadFileForm()
        pass

    

    # Render list page with the documents and the form
    return render_to_response(
        'admin/linksimport.html',
        {'form': form},
        context_instance=RequestContext(request)
    )    