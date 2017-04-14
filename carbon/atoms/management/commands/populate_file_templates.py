import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from carbon.utils.template import get_page_templates, get_page_templates_raw

from ...models import Template


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):

        #Create file templates if any are missing
        
        template_dirs = settings.TEMPLATES[0]['DIRS']

        for template_dir in template_dirs:
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    
                    template, created = Template.objects.get_or_create(file_template = file)
                    if not template.title or 'untitled' in template.title.lower():
                        template.title = u'File Template %s'%(file)
                        template.save()
                    

