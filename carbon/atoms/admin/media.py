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

from .content import *

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
    autocomplete_lookup_fields = {
        'fk': (),
        'm2m': ('tags',)
    }
    raw_id_fields = ( 'tags',)

    
    search_fields = ('title', 'alt', 'caption', 'credit')
    list_filter = ('tags', "created_by", "modified_by", )
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

class BaseImageAdmin(BaseMedia, BaseVersionableAdmin):

    change_list_template = "admin/media/change_list_image.html"

    def preview(self, obj):
        if obj.image:
            try:
                return "<img src='%s' alt='%s preview'/>"%(obj.thumbnail.url, obj.title)
            except:
                return ""
        return ''
    preview.allow_tags = True

    def tag_list(self, obj):
        
        output = ''
        all_tags = obj.tags.all()
        if len(all_tags) > 1:
            output += '<span>Tags: </span>'

        elif len(all_tags) > 0:
            output += '<span>Tag: </span>'

        for tag in all_tags:
            output += ('<a href="?tags__id__exact=%s">%s</a> '%(tag.pk, tag.title))
        return output

    tag_list.allow_tags = True

    def image_variants(self, obj):

        if obj.image:
            base_image =  '<a href="%s" target="_blank">Original Size (%spx x %spx)</a><br />'%(obj.image_url, obj.image_width, obj.image_height)
            for variant in obj.__class__.variants:
                image_variant_name = variant.replace("_", " ").title()
                base_image +=  '<a href="%s" target="_blank">%s (%spx x %spx)</a><br />'%(obj.get_variant_url(variant), image_variant_name, obj.get_variant_width(variant), obj.get_variant_height(variant))

            return base_image
    image_variants.allow_tags = True


    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "preview", "image_variants", "tag_list"
    )
    
    core_fields = (
        'title',
        ('image','preview'),
        ('image_variants'),
        ('clean_filename_on_upload','allow_overwrite'),
        ('alt','use_png'),
        'credit',
        'caption',
        'tags'

    )
    

    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Image", {
            'fields': core_fields,
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    list_display = ('title','preview','image_width', 'image_height', 'display_size', 'tag_list')
    list_display_links = ('title', 'preview')



class BaseMediaAdmin(BaseMedia, BaseVersionableAdmin):


    readonly_fields = BaseVersionableAdmin.readonly_fields
    
    core_fields = (
        'title',
        ('file','image'),
        ('clean_filename_on_upload','allow_overwrite'),
        'credit',
        'caption',
        'tags'

    )

    meta_fields = BaseVersionableAdmin.meta_fields

    fieldsets = (
        ("Image", {
            'fields': core_fields,
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    list_display = ('title','file','display_size', 'size')
    list_filter = ('tags',)
