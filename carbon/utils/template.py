from os import path
from glob import glob
import os
import fnmatch
import re

from django.conf import settings

def get_page_templates_raw(ignore_templates = None):

    if not ignore_templates:
        ignore_templates = ()

    files = []
    template_dirs = settings.TEMPLATE_DIRS
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

    template_dirs = settings.TEMPLATE_DIRS
    for template_dir in template_dirs:
        
        def name(n):
            return n.replace(template_dir, '')\
                .replace('_', ' ')\
                .replace('.html', '')\
                .replace("-", " ")\
                .replace("/", " - ").title()
        output += [(i, name(i)) for i in raw_templates]

    return output