from django.conf import settings
from django.contrib.sitemaps import Sitemap

class AddressibleSitemap(Sitemap):    

    def items(self):        
        return self.model.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()        

    def lastmod(self, obj):
        return obj.modified_date