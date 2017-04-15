"""
Wrapper for loading templates from the filesystem.
"""

import io

from django.core.exceptions import SuspiciousFileOperation
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join
from django.template import Template as DjangoTemplate
try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:  # Django < 1.9
    from django.template.loader import BaseLoader


from .models import Template

from carbon.utils.template import get_template_by_pk_or_slug

class DBTemplateLoader(BaseLoader):
    is_usable = True

    
    def load_template(self, template_name, template_dirs=None):
        # print 'get template: %s'%(template_name)
        template = get_template_by_pk_or_slug(template_name)
        if template:
            return DjangoTemplate(template.get_content()), template_name
            
        raise TemplateDoesNotExist("No existe template %s"%(template_name))


    def load_template_source(self, template_name, template_dirs=None):
        # print 'load template source %s'%(template_name)
        template = self.load_template(template_name, template_dirs=None)
        if template:
            return template.get_content(), template_name

        raise TemplateDoesNotExist("No existe template %s"%(template_name))
    load_template_source.is_usable = True


    # #HACK -- argument incompatibility
    # def __init__(self, *args):
    #     kwargs = {}
    #     super(DBTemplateLoader, self).__init__(self, *args, **kwargs) 

    
