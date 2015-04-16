from carbon.atoms.admin.taxonomy import *
from carbon.atoms.admin.media import *

# from .models import *


class MediaTagAdmin(BaseTagAdmin):
    pass

class ImageAdmin(BaseImageAdmin):

    
    extra_urls = [
        {'url':reverse_lazy('admin_image_batch_view'), 'title':'Batch Upload Images'}
    ]
    batch_response = batch_upload_image_response

    


class SecureImageAdmin(BaseImageAdmin):

    extra_urls = [
        {'url':reverse_lazy('admin_secureimage_batch_view'), 'title':'Batch Upload Secure Images'}
    ]
    batch_response = batch_upload_image_response



class MediaAdmin(BaseMediaAdmin):

    extra_urls = [
        {'url':reverse_lazy('admin_document_batch_view'), 'title':'Batch Upload Media'}
    ]
    batch_response = batch_upload_media_response

class SecureMediaAdmin(BaseMediaAdmin):
    
    extra_urls = [
        {'url':reverse_lazy('admin_securedocument_batch_view'), 'title':'Batch Upload Secure Media'}
    ]
    batch_response = batch_upload_media_response



# admin.site.register(Image, ImageAdmin)
# admin.site.register(SecureImage, SecureImageAdmin)    
# admin.site.register(Media, MediaAdmin)    
# admin.site.register(SecureMedia, SecureMediaAdmin)    