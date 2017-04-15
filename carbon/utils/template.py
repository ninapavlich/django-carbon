from os import path
from glob import glob
import os
import fnmatch
import re

from django.conf import settings
from django.core.cache import cache
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

try:
    # Django >= 1.8
    from django.template.loaders.app_directories import get_app_template_dirs
    app_template_dirs = get_app_template_dirs('templates')
except AttributeError:
    # Django <= 1.7
    from django.template.loaders.app_directories import app_template_dirs




def get_page_templates_raw(ignore_templates = None):

    if not ignore_templates:
        ignore_templates = ()

    files = []
    template_dirs = settings.TEMPLATES[0]['DIRS']
    for template_dir in template_dirs:
        for root, dirnames, filenames in os.walk(template_dir):
            for filename in fnmatch.filter(filenames, '*.html'):
                raw_file_name = os.path.join(root, filename)
                simple_path = raw_file_name.replace(template_dir+"/", "")
                files.append(str(simple_path))

    return files

def get_page_templates(ignore_templates = None):

    raw_templates = get_page_templates_raw(ignore_templates)
    output = []

    template_dirs = settings.TEMPLATES[0]['DIRS']
    for template_dir in template_dirs:
        
        def name(n):
            return n.replace(template_dir, '')\
                .replace('_', ' ')\
                .replace('.html', '')\
                .replace("-", " ")\
                .replace("/", " - ").title()
        output += [(i, name(i)) for i in raw_templates]

    return output


def get_all_templates():
   
    template_files = []
    for template_dir in (settings.TEMPLATES[0]['DIRS'] + app_template_dirs):
        for dir, dirnames, filenames in os.walk(template_dir):
            for filename in filenames:
                template_files.append(os.path.join(dir, filename))

    return template_files

def get_template_cache_key(template_pk_or_slug):
    return 'carbon_template_'+template_pk_or_slug

def get_template_by_pk_or_slug(template_pk_or_slug):

    found_template = None
    try:
        app_label = settings.TEMPLATE_MODEL.split('.')[0]
        object_name = settings.TEMPLATE_MODEL.split('.')[1]
        model = get_model(app_label, object_name)


        found_template = cache.get( get_template_cache_key(template_pk_or_slug) )
        
        if not found_template:

            if isinstance( template_pk_or_slug, ( int, long ) ):
                #try by pk
                try:
                    found_template = model.objects.get(pk=template_pk_or_slug)
                except:
                    pass

            if found_template == None:
                #try by slug
                try:
                    found_template = model.objects.get(slug=template_pk_or_slug)
                except:
                    pass

            #TRY WITH DB PREFIX
            prefix = 'template_'
            if found_template == None:
                #try by slug
                unprefixed_slug = template_pk_or_slug.replace(prefix, '')
                try:
                    found_template = model.objects.get(slug=unprefixed_slug)
                except:
                    pass

            cache.set(get_template_cache_key(template_pk_or_slug), found_template, settings.CACHE_DURATION)
            
    except:
        pass

    

    return found_template    