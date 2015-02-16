from django.conf.urls import patterns, url, include

from .views import admin_import_links


urlpatterns = patterns('',
	
	# url(r'^tags/(?P<path>[\w-]+)/$', PageTagView.as_view(), name='pages_tag'),
	# url(r'^(?P<path>[-_\/\w]*)$', PageDetail.as_view(), name="pages_page"),
	# url(r'^(?P<path>.*)$', PageDetail.as_view(), name="pages_page"),

	url(r'^admin/utils/import/links/$', admin_import_links, name='admin_import_links'),
)