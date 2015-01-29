from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()



sitemaps = {}

urlpatterns = patterns('')


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        (r'', include('example.urls_favicons')),
    )

urlpatterns +=  patterns('',
    
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^ckeditor/', include('ckeditor.urls')),

    #(r'^robots\.txt$', include('robots.urls')),

    # -- Pages
    url(r'^', include('carbon.compounds.portfolio.urls')),
    url(r'^', include('carbon.compounds.page.urls')),

    # - Static URLS
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG and settings.STATIC_ROOT:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






