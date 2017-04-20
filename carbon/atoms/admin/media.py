import json
from mimetypes import MimeTypes
import urllib

from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, resolve
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_protect
from django.utils.safestring import mark_safe


from .content import *

csrf_protect_m = method_decorator(csrf_protect)



class TagListFilter(SimpleListFilter):
    title = 'tag'
    parameter_name = 'tag'
    def lookups(self, request, model_admin):

      tags = model_admin.tag_model.objects.all()
      items = ()
      for tag in tags:
        items += ((str(tag.id), str(tag.title),),)
      return items

    def queryset(self, request, queryset):
      tag_id = request.GET.get(self.parameter_name, None)
      if tag_id:
        return queryset.filter(tags=tag_id)
      return queryset

class FolderListFilter(SimpleListFilter):
    title = 'folder'
    parameter_name = 'folder'
    def lookups(self, request, model_admin):

        folders = model_admin.folder_model.objects.all()
        items = ()
        for folder in folders:
            items += ((str(folder.id), str(folder.title_path),),)

        items += ((str(-1), "Items in any or all folders",),)
        return items

    def queryset(self, request, queryset):
      folder_id = request.GET.get(self.parameter_name, None)
      if folder_id:
        return queryset.filter(folder=folder_id)
      return queryset


class BaseMedia(object):
    # autocomplete_lookup_fields = {
    #     'fk': ('folder'),
    #     'm2m': ('tags',)
    # }
    # raw_id_fields = ( 'tags','folder')

    
    search_fields = ('title', 'alt', 'caption', 'credit')
    change_list_template = "admin/media/change_list.html"

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        response = super(BaseMedia, self).changelist_view(request, extra_context)
    
        try:
            context_data = response.context_data
            context_data['extra_urls'] = self.extra_urls
        except:
            pass 
        
        return response



class FolderTagAdmin(admin.ModelAdmin):

    change_list_template = "admin/media/change_list_image_folders.html"
    
    def get_folder_qs(self, request, folder_id=None):
        if folder_id is None:
          folder_id = request.POST.get('folder__id__exact', None) or request.POST.get('folder_id', None) or request.POST.get('folder', None)

        if folder_id is None:
            folder_id = request.GET.get('folder__id__exact', None) or request.GET.get('folder_id', None) or request.GET.get('folder', None)

        if folder_id=="None":
            folder_id=None

        return folder_id

    def get_tag_qs(self, request, tag_id=None):
        if tag_id is None:
          tag_id = request.POST.get('tag__id__exact', None) or request.POST.get('tag_id', None) or request.POST.get('tag', None)

        if tag_id is None:
            tag_id = request.GET.get('tag__id__exact', None) or request.GET.get('tag_id', None) or request.GET.get('tag', None)

        return tag_id

    def get_folder(self, request, folder_id=None):
        
        folder_id = self.get_folder_qs(request, folder_id)

        if folder_id and int(folder_id) >= 0:

            return self.folder_model.objects.get(pk=folder_id)
        return None

    def get_tag(self, request, tag_id=None):
        
        tag_id = self.get_tag_qs(request, tag_id)

        if tag_id and int(tag_id) >= 0:

            return self.tag_model.objects.get(pk=tag_id)
        return None
    
    def get_add_folder_url(self, request):

        url = reverse('admin:%s_%s_add'%(self.folder_model._meta.app_label.lower(), self.folder_model._meta.object_name.lower()))  

        current_folder = self.get_folder(request)
        if current_folder:
            current_url = request.get_full_path()
            url = '%s?%s'%(url, urlencode({'parent': current_folder.pk, '_redirect_to':current_url}))

        return url

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



    def get_all_tags(self):
        return self.tag_model.objects.all()

    def tag_list(self, obj):
        
        output = ''
        all_tags = obj.tags.all()
        if len(all_tags) > 1:
            output += '<strong>Tags: </strong>'

        elif len(all_tags) > 0:
            output += '<strong>Tag: </strong>'

        for tag in all_tags:
            output += ('<a href="?tags__id__exact=%s">%s</a> '%(tag.pk, tag.title))
        return mark_safe(output)

        

    def get_queryset(self, request):
        qs = super(FolderTagAdmin, self).get_queryset(request)
        
        if 'changelist' in resolve(request.path).url_name:
            ignore_folders = self.ignore_folders(request)
            folder = self.get_folder(request)

            if folder is None and ignore_folders is False:
                qs = qs.filter(folder=None)


        return qs

    def move_to_folder(self, request, queryset):        

        if request.POST.get('post', None):

            folder = self.get_folder(request, request.POST.get('folder', None))
            
            count = len(queryset)
            for item in queryset:
                item.folder = folder
                print 'set folder to %s on %s'%(item.folder, item)
                item.save()

            if folder:
                #Redirect to folder that items were moved to...
                get = request.GET.copy()
                get['folder__id__exact'] = folder.pk
                path = '%s?' % request.path
                for query, val in get.items():
                    path += '%s=%s&' % (query, val)
                redirect_url = path[:-1]  
                messages.success(request, u'%s items moved to folder %s'%(count, folder))

            else:
                redirect_url = request.get_full_path()
                messages.success(request, u'%s items moved to the top-level, out of all folders'%(count))

          
            return HttpResponseRedirect(redirect_url)

        else:

            return render_to_response('admin/media/move_to_folder.html', 
            {
                'queryset': queryset, 
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'folders':self.get_all_folders()
            }, 
            context_instance=RequestContext(request))

        move_to_folder.short_description = "Move to folder..."

    def tag_items(self, request, queryset):        

        if request.POST.get('post', None):

            tag = self.get_tag(request, request.POST.get('tag', None))
            
            

            if tag:

                count = len(queryset)
                for item in queryset:
                    item.tags.add(tag)
                    item.save()

                messages.success(request, u'%s items tagged with %s'%(count, tag))
          
            redirect_url = request.get_full_path()
            return HttpResponseRedirect(redirect_url)

        else:

            return render_to_response('admin/media/tag_items.html', 
            {
                'queryset': queryset, 
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'tags':self.get_all_tags()
            }, 
            context_instance=RequestContext(request))

        tag_items.short_description = "Tag items..."

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        current_folder = self.get_folder(request)
        extra_context['folders'] = self.get_folders(current_folder)
        extra_context['current_folder'] = current_folder
        extra_context['add_folder_url'] = self.get_add_folder_url(request)
        extra_context['ignore_folders'] = self.ignore_folders(request)
        return super(FolderTagAdmin, self).changelist_view(request, extra_context=extra_context)


    autocomplete_lookup_fields = {
        'fk': ('folder',),
        'm2m': ('tags',)
    }
    raw_id_fields = ( 'tags','folder')

    list_filter = BaseVersionableAdmin.list_filter + (TagListFilter, FolderListFilter,)
    actions = [move_to_folder, tag_items]

    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "display_size", "size", "dimensions", "tag_list"
    )

class BaseImageAdmin(BaseMedia, BaseVersionableAdmin):

    change_list_template = "admin/media/change_list_image.html"

    def preview(self, obj):
        if obj.image:
            try:
                return mark_safe("<img src='%s' alt='%s preview'/>"%(obj.thumbnail.url, obj.title))
            except:
                return ""
        return ''

    

    def image_variants(self, obj):
        if obj.image:
            base_image =  '<a href="%s" target="_blank">Original Size (%spx x %spx)</a><br />'%(obj.image_url, obj.image_width, obj.image_height)
            for variant in obj.__class__.variants:
                image_variant_name = variant.replace("_", " ").title()
                base_image +=  '<a href="%s" target="_blank">%s (%spx x %spx)</a><br />'%(obj.get_variant_url(variant), image_variant_name, obj.get_variant_width(variant), obj.get_variant_height(variant))

            return mark_safe(base_image)
    

    def image_variants_links(self, obj):

        if obj.image:
            base_image =  '<a href="%s" target="_blank">Original Size (%spx x %spx)</a><br />'%(obj.image_url, obj.image_width, obj.image_height)
            for variant in obj.__class__.variants:
                image_variant_name = variant.replace("_", " ").title()
                base_image +=  '<a href="%s" target="_blank">%s</a><br />'%(obj.get_variant_url(variant), image_variant_name)

            return mark_safe(base_image)
    

    def dimensions(self, obj):
        if obj.image:
            return mark_safe('Original Dimensions: %sx%s Size: %s'%(obj.image_width, obj.image_height, obj.display_size))
            return mark_safe(base_image)


    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "preview", "image_variants", "image_width", "image_height",
        "display_size", "size", "dimensions", "file_modified_date"
    )
    
    core_fields = (
        'title',
        ('image','preview'),
        ('dimensions'),
        ('image_variants'),
        ('clean_filename_on_upload','allow_overwrite'),
        ('alt','use_png'),
        'credit',
        'caption'
    )
    
    meta_fields = (
        ('version',),
        ('created_date', 'created_by'),
        ('modified_date', 'modified_by'),
        'file_modified_date',
        'admin_note'
    )
    

    fieldsets = (
        ("Image", {
            'fields': core_fields,
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    list_display = ('title','preview','image_width', 'image_height', 'display_size',)
    list_display_links = ('title', 'preview')



class BaseMediaAdmin(BaseMedia, BaseVersionableAdmin):


    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "file_modified_date"
    )   

    
    core_fields = (
        'title',
        ('file',),
        ('clean_filename_on_upload','allow_overwrite'),
        'credit',
        'caption'
    )

    meta_fields = (
        ('version',),
        ('created_date', 'created_by'),
        ('modified_date', 'modified_by'),
        'file_modified_date',
        'admin_note'
    )

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
    

class BaseSecureMediaAdmin(BaseMediaAdmin):
    def secure_url(self, obj):
        duration = 120
        url = obj.get_secure_url(duration)
        if url:
            return mark_safe("<a href='%s'>Download</a><br /><br />This link will expire after %s seconds.</a>"%(url, duration))
        return ''

    readonly_fields = (
        "version", "created_date", "created_by", "modified_date", "modified_by",
        "secure_url"
    )  
    core_fields = (
        'title',
        ('file','secure_url'),
        ('clean_filename_on_upload','allow_overwrite'),
        'credit',
        'caption',
    )
    meta_fields = (
        ('version',),
        ('created_date', 'created_by'),
        ('modified_date', 'modified_by'),
        'file_modified_date',
        'admin_note'
    )

    fieldsets = (
        ("Image", {
            'fields': core_fields,
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )


