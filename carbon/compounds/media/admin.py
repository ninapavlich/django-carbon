from django.contrib import admin

from carbon.atoms.admin.media import *
# from .models import *



class ImageAdmin(BaseImageAdmin):
    pass

class SecureImageAdmin(BaseImageAdmin):
    pass    


class MediaAdmin(BaseMediaAdmin):
    pass

class SecureMediaAdmin(BaseMediaAdmin):
    pass


# admin.site.register(Image, ImageAdmin)
# admin.site.register(SecureImage, SecureImageAdmin)    
# admin.site.register(Media, MediaAdmin)    
# admin.site.register(SecureMedia, SecureMediaAdmin)    