from django.conf.urls.static import static
from django.conf.urls import patterns, url, include
from django.conf import settings

from django.views.generic import TemplateView, RedirectView

#who knew that there were so many favicons??
urlpatterns = patterns('',
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=False)),  
    (r'^favicon\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.png', permanent=False)),  
    
    (r'^apple-touch-icon-57x57\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-57x57.png', permanent=False)),  
    (r'^apple-touch-icon-60x60\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-60x60.png', permanent=False)),  
    (r'^apple-touch-icon-72x72\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-72x72.png', permanent=False)),  
    (r'^apple-touch-icon-76x76\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-76x76.png', permanent=False)),  
    (r'^apple-touch-icon-114x114\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-114x114.png', permanent=False)),  
    (r'^apple-touch-icon-120x120\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-120x120.png', permanent=False)),  
    (r'^apple-touch-icon-144x144\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-144x144.png', permanent=False)),  
    (r'^apple-touch-icon-152x152\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-152x152.png', permanent=False)),  
    (r'^apple-touch-icon-precomposed\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-precomposed.png', permanent=False)),  
    (r'^favicon-16x16\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-16x16.png', permanent=False)),  
    (r'^favicon-32x32\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-32x32.png', permanent=False)),  
    (r'^favicon-96x96\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-96x96.png', permanent=False)),  
    (r'^favicon-160x160\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-160x160.png', permanent=False)),  
    (r'^favicon-192x192\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-192x192.png', permanent=False)),  
    (r'^mstile-70x70\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-70x70.png', permanent=False)),  
    (r'^mstile-144x144\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-144x144.png', permanent=False)),  
    (r'^mstile-150x150\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-150x150.png', permanent=False)),  
    (r'^mstile-310x150\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-310x150.png', permanent=False)),  
    (r'^mstile-310x310\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-310x310.png', permanent=False)),  

    (r'^social-icon\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'social-icon.png', permanent=False)),  
    
)
