from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

from django_batch_uploader.views import AdminBatchUploadView

from .models import *

class BasePickerView(ListView):
    
    
    paginate_by = 48
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated() and self.request.user.is_staff:
            
            if 'q' in self.request.GET and self.request.GET['q']!= '':
                query = self.request.GET['q']
                queryset = self.model.objects.filter(
                    Q(title__icontains=query) |
                    Q(caption__icontains=query) | 
                    Q(credit__icontains=query) | 
                    Q(admin_note__icontains=query) ).order_by('-id')    
            else:
                queryset = self.model.objects.all().order_by('-id')

            return queryset

        else:

            raise PermissionDenied

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BasePickerView, self).dispatch(*args, **kwargs)

class ImagePickerView(BasePickerView):
    template_name = "admin/media/image_picker.html"
    model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])



class ImageBatchView(AdminBatchUploadView):      

    # model = Image

    #Media file name
    media_file_name = 'image'

    #Which fields can be applied in bulk?
    default_fields = ['credit', 'tags']

    #Which fields can be applied individually?
    detail_fields = ['title', 'alt', 'caption', 'use_png']

    default_values = {}

class SecureImageBatchView(ImageBatchView):      
    
    # model = SecureImage
    pass


class DocumentBatchView(AdminBatchUploadView):      
    
    # model = Document

    #Media file name
    media_file_name = 'file'

    #Which fields can be applied in bulk?
    default_fields = ['credit', 'tags']

    #Which fields can be applied individually?
    detail_fields = ['title',  'caption']

    default_values = {}

class SecureDocumentBatchView(DocumentBatchView):      
    
    # model = SecureDocument
    pass

