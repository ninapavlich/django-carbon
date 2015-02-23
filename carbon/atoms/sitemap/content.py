from django.conf import settings
from django.contrib.sitemaps import Sitemap

from .abstract import AddressibleSitemap

class PublishableSitemap(AddressibleSitemap):    

    def items(self):   
    	all_items = self.model.objects.published()
    	return [item for item in all_items if item.is_published()]

class SEOSitemap(PublishableSitemap):    

    def priority(self, obj):
        return obj.sitemap_priority

    def changefreq(self, obj):
        return obj.sitemap_changefreq        