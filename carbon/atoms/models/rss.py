import re
from bs4 import BeautifulSoup
import datetime
import feedparser
import pytz
import requests
from time import mktime

from django.core.exceptions import ImproperlyConfigured
from django.db import models

from .abstract import VersionableAtom, TitleAtom
from .content import PublishableAtom

class RSSSourceMolecule( VersionableAtom, TitleAtom ):

    #content_model = RSSEntryAtom
    
    url = models.CharField(max_length=255, null=True, blank=True)

    active = models.BooleanField(default=True)

    last_imported = models.DateTimeField(blank=True, null=True)

    logo_url = models.CharField(max_length=255, null=True, blank=True)
    logo_width = models.CharField(max_length=255, null=True, blank=True)
    logo_height = models.CharField(max_length=255, null=True, blank=True)

    regex = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True  

    def __unicode__(self):
        return self.url

    def sync_rss(self):

        if not self.active:
            return

        response = requests.get(self.url)
        raw_xml = response.text

        feed = feedparser.parse(raw_xml)
        for entry_element in feed.entries:   
            do_import = self.import_entry(entry_element)
            if do_import:
                content_object = self.parse_entry(entry_element)

        self.last_imported = datetime.datetime.now()
        self.save()

    def get_entry_uuid(self, entry_element):
        return self.url+entry_element.id

    def import_entry(self, entry_element):
        content = entry_element.content[0].value
        if self.regex:
            prog = re.compile(self.regex, re.M|re.I)
            match = prog.match( content )

            if match:
               return True
            else:
               return False
        #OR Override in subclass

        return True

    def set_image(self, content_object, url):
        #Override in subclass
        return None
    
    
    def parse_entry(self, entry_element):   

        if not self.content_model:
            raise ImproperlyConfigured( "Model should define content_model")     

        
        synopsis = None
        if 'description' in entry_element:
            synopsis = entry_element.description
        elif 'summary' in entry_element:
            synopsis = entry_element.summary

        content = entry_element.content[0].value

        utc=pytz.UTC
        if entry_element.published_parsed:
            date = utc.localize(datetime.datetime.fromtimestamp(mktime(entry_element.published_parsed)))
        else:
            date = utc.localize(datetime.datetime.now())            

        entry, created = self.content_model.objects.get_or_create(
            rss_url=self,
            uuid = self.get_entry_uuid(entry_element)
        )

        if created:
            entry.publication_status = PublishableAtom.PUBLISHED
            entry.title = entry_element.title
            entry.slug = entry_element.id
            entry.publication_date = date
            entry.synopsis = synopsis
            entry.content = content
            entry.path_override = entry_element.link  
            entry.save()

        
            model_has_image = hasattr(self.content_model, 'image')
            if model_has_image:
                image_url = None if (not model_has_image or not 'image' in entry_element) else entry_element.image['href']
                if not image_url:
                    
                    soup = BeautifulSoup(content)
                    content_images = [image["src"] for image in soup.findAll("img")]
                    if(len(content_images) > 0):
                        image_url = content_images[0]
                        self.set_image(entry, image_url)
            



        return entry
