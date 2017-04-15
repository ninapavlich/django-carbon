from django.conf.urls.static import static
from django.conf.urls import include, url

from django.views.generic import TemplateView

from django.contrib.admindocs import views

from .views import *
from .views_admindocs import *

urlpatterns = [
    
    
    url(r'^admin/utils/cache/clear/', clear_cache, name="clear-server-cache"),
    url(r'^admin/grappelli/lookup/autocomplete/$', FilteredAutocomplete.as_view(), name="grp_autocomplete_lookup"),
    url('^admin/doc/models/(?P<app_label>[^\.]+)\.(?P<model_name>[^/]+)/$',
        custom_model_detail,
        name='django-admindocs-models-detail'
    ),

    url(r'^error_403/', TemplateView.as_view(template_name="403.html"), name="error_403_preview" ),
    url(r'^error_404/', TemplateView.as_view(template_name="404.html"), name="error_404_preview" ),
    url(r'^error_405/', TemplateView.as_view(template_name="405.html"), name="error_405_preview" ),
    url(r'^error_500/', TemplateView.as_view(template_name="500.html"), name="error_500_preview" ),
    url(r'^error_501/', TemplateView.as_view(template_name="501.html"), name="error_501_preview" ),

    url(r'^error_maintenance/', TemplateView.as_view(template_name="maintenance.html"), name="error_maintenance_preview" ),    
    
]