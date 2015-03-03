import json
from mimetypes import MimeTypes
import urllib

from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from carbon.atoms.admin.media import *

# from .models import *

csrf_protect_m = method_decorator(csrf_protect)


def batch_upload_image_response(self, request):
    try:
        latest_log_entry = LogEntry.objects.filter(action_flag=ADDITION).order_by('-action_time')[0]
        ct = ContentType.objects.get_for_id(latest_log_entry.content_type_id)
        obj = ct.get_object_for_this_type(pk=latest_log_entry.object_id)
        if obj:
            
            mime = MimeTypes()
            url = urllib.pathname2url(obj.image_url)
            mime_type = mime.guess_type(url)
            data = {
                "files":[
                    {
                        "url": obj.image_url,
                        "thumbnailUrl": obj.thumbnail.url,
                        "name": obj.title,
                        "type": mime_type[0],
                        "size": obj.image.size
                    }
                ]
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        return None


def batch_upload_media_response(self, request):
    try:
        latest_log_entry = LogEntry.objects.filter(action_flag=ADDITION).order_by('-action_time')[0]
        ct = ContentType.objects.get_for_id(latest_log_entry.content_type_id)
        obj = ct.get_object_for_this_type(pk=latest_log_entry.object_id)
        if obj:
            
            mime = MimeTypes()
            url = urllib.pathname2url(obj.media_url)
            mime_type = mime.guess_type(url)
            data = {
                "files":[
                    {
                        "url": obj.media_url,
                        "thumbnailUrl": obj.image_thumbnail_url,
                        "name": obj.title,
                        "type": mime_type[0],
                        "size": obj.media.size
                    }
                ]
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        return None

class BaseMedia(object):
    
    change_list_template = "admin/media/change_list.html"

    def add_view(self, request, form_url='', extra_context=None):
        default_response = super(BaseMedia, self).add_view(request, form_url, extra_context)
        if request.method == 'POST' and "batch" in request.POST:

            response = self.batch_response(request)
            if response != None:
                return response

        return default_response

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        response = super(BaseMedia, self).changelist_view(request, extra_context)
        
        try:
            context_data = response.context_data
            context_data['extra_urls'] = self.extra_urls
        except:
            pass
            
        return response


class ImageAdmin(BaseMedia, BaseImageAdmin):

    
    extra_urls = [
        {'url':reverse_lazy('admin_image_batch_view'), 'title':'Batch Upload Images'}
    ]
    batch_response = batch_upload_image_response

    


class SecureImageAdmin(BaseMedia, BaseImageAdmin):

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