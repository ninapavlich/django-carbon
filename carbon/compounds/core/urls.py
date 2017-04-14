from django.conf.urls import include, url

from .views import admin_import_links

urlpatterns = [
	
	url(r'^admin/utils/import/links/$', admin_import_links, name='admin_import_links'),
]