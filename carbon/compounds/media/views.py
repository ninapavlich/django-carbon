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

class ImagePickerFolderView(BasePickerView):
    template_name = "admin/media/image_picker_folders.html"
    model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])    

    def get_folder_qs(self, request, folder_id=None):
        if folder_id is None:
          folder_id = request.POST.get('folder__id__exact', None) or request.POST.get('folder_id', None) or request.POST.get('folder', None)

        if folder_id is None:
            folder_id = request.GET.get('folder__id__exact', None) or request.GET.get('folder_id', None) or request.GET.get('folder', None)

        if folder_id=="None":
            folder_id=None

        return folder_id

    def get_folder(self, request, folder_id=None):
        
        folder_id = self.get_folder_qs(request, folder_id)
        if folder_id and int(folder_id) >= 0:
            return self.folder_model.objects.get(pk=folder_id)
        return None

    def ignore_folders(self, request):
        has_query = request.GET.get('q', None) != None
        folder_id = self.get_folder_qs(request)
        if has_query and not folder_id:
            return True

        
        if folder_id and int(folder_id) < 0:
            return True

        return False

    def get_folders(self, current_folder=None):
        if current_folder:
            return self.folder_model.objects.filter(parent=current_folder)
        else:
            return self.folder_model.objects.filter(parent=None)

    def get_all_folders(self):
        return self.folder_model.objects.all()

    def get_queryset(self):
        qs = super(ImagePickerFolderView, self).get_queryset()
        
        ignore_folders = self.ignore_folders(self.request)
        folder = self.get_folder(self.request)

        if folder is None and ignore_folders is False:
            qs = qs.filter(folder=None)
        elif folder:
            qs = qs.filter(folder=folder)

        return qs

    def get_context_data(self, **kwargs):
        context = super(ImagePickerFolderView, self).get_context_data(**kwargs)
        request = self.request

        current_folder = self.get_folder(request)
        context['folders'] = self.get_folders(current_folder)
        context['current_folder'] = current_folder
        context['ignore_folders'] = self.ignore_folders(request)
        context['top_url'] = self.request.path
        return context

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

