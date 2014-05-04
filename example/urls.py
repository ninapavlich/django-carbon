from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()



sitemaps = {}

urlpatterns = patterns('',
    
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    

    #(r'^admin/utils/travel/update$', 'mikeandnina.kernel.api.google_flights.update' ),

    (r'^admin/', include(admin.site.urls)),


    # - Static URLS
    (r'', include('example.urls_favicons')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)