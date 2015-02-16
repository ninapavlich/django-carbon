from django.conf import settings
from django.contrib.sitemaps import Sitemap

from .abstract import AddressibleSitemap

class PublishableSitemap(AddressibleSitemap):    

    def items(self):        
        return self.model.objects.published()

class SEOSitemap(PublishableSitemap):    

    def priority(self, obj):
        return obj.sitemap_priority

    def changefreq(self, obj):
        return obj.sitemap_changefreq        