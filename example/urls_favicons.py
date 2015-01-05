from django.conf.urls import patterns, url
from django.conf import settings

from django.views.generic import RedirectView

#See realfavicongenerator.net for updated favicon list
urlpatterns = patterns('',
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),  
    (r'^favicon\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.png')),  
    
    (r'^apple-touch-icon-57x57\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-57x57.png')),  
    (r'^apple-touch-icon-60x60\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-60x60.png')),  
    (r'^apple-touch-icon-72x72\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-72x72.png')),  
    (r'^apple-touch-icon-76x76\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-76x76.png')),  
    (r'^apple-touch-icon-114x114\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-114x114.png')),  
    (r'^apple-touch-icon-120x120\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-120x120.png')),  
    (r'^apple-touch-icon-144x144\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-144x144.png')),  
    (r'^apple-touch-icon-152x152\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-152x152.png')),  
    (r'^apple-touch-icon-precomposed\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'apple-touch-icon-precomposed.png')),  
    
    (r'^favicon-16x16\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-16x16.png')),  
    (r'^favicon-32x32\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-32x32.png')),  
    (r'^favicon-96x96\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-96x96.png')),  
    (r'^favicon-160x160\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-160x160.png')),  
    (r'^favicon-192x192\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-192x192.png')),  
    
    (r'^mstile-70x70\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-70x70.png')),  
    (r'^mstile-144x144\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-144x144.png')),  
    (r'^mstile-150x150\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-150x150.png')),  
    (r'^mstile-310x150\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-310x150.png')),  
    (r'^mstile-310x310\.png$', RedirectView.as_view(url=settings.STATIC_URL + 'mstile-310x310.png')),  
)
