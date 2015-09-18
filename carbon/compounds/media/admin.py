from django.core.urlresolvers import reverse_lazy

from carbon.atoms.admin.taxonomy import *
from carbon.atoms.admin.media import *

# from .models import *


from django_batch_uploader.admin import BaseBatchUploadAdmin

class MediaTagAdmin(BaseTagAdmin):
    pass

class ImageAdmin(BaseImageAdmin, BaseBatchUploadAdmin):

    
    extra_urls = [
        {'url':reverse_lazy('admin_image_batch_view'), 'title':'Batch Upload Images'}
    ]
    
    


class SecureImageAdmin(BaseImageAdmin, BaseBatchUploadAdmin):

    extra_urls = [
        {'url':reverse_lazy('admin_secureimage_batch_view'), 'title':'Batch Upload Secure Images'}
    ]
    



class MediaAdmin(BaseBatchUploadAdmin, BaseMediaAdmin):

    extra_urls = [
        {'url':reverse_lazy('admin_document_batch_view'), 'title':'Batch Upload Media'}
    ]
    

class SecureMediaAdmin(BaseMediaAdmin, BaseBatchUploadAdmin):
    
    extra_urls = [
        {'url':reverse_lazy('admin_securedocument_batch_view'), 'title':'Batch Upload Secure Media'}
    ]



# admin.site.register(Image, ImageAdmin)
# admin.site.register(SecureImage, SecureImageAdmin)    
# admin.site.register(Media, MediaAdmin)    
# admin.site.register(SecureMedia, SecureMediaAdmin)    