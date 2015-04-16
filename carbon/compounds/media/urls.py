from django.conf.urls.static import static
from django.conf.urls import patterns, url, include

from .views import *

urlpatterns = patterns('',
    
    url(r'admin/media/imagepicker/$', ImagePickerView.as_view(), name="admin_imagepicker_view"), 
    
    url(r'admin/media/images/batch/$', ImageBatchView.as_view(), name="admin_image_batch_view"), 
    url(r'admin/media/secureimages/batch/$', SecureImageBatchView.as_view(), name="admin_secureimage_batch_view"), 
    url(r'admin/media/documents/batch/$', DocumentBatchView.as_view(), name="admin_document_batch_view"), 
    url(r'admin/media/securedocuments/batch/$', SecureDocumentBatchView.as_view(), name="admin_securedocument_batch_view"), 

)

