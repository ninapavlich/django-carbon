from django.contrib import admin

from carbon.compounds.media.admin import ImageAdmin as BaseImageAdmin
from carbon.compounds.media.admin import SecureImageAdmin as BaseSecureImageAdmin
from carbon.compounds.media.admin import MediaAdmin as BaseMediaAdmin
from carbon.compounds.media.admin import SecureMediaAdmin as BaseSecureMediaAdmin

from .models import *

class ImageAdmin(BaseImageAdmin):
    pass

class SecureImageAdmin(BaseSecureImageAdmin):
    pass    


class MediaAdmin(BaseMediaAdmin):
    pass

class SecureMediaAdmin(BaseSecureMediaAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(SecureImage, SecureImageAdmin)    
admin.site.register(Media, MediaAdmin)    
admin.site.register(SecureMedia, SecureMediaAdmin)        