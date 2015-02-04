from django.conf.urls import patterns, url, include

from .views import *


# urlpatterns = patterns('',
	
# 	url(r'^projects/categories/(?P<path>[\w-]+)/$', ProjectCategoryView.as_view(), name='projects_category'),
# 	url(r'^projects/(?P<path>[\w-]+)/$', ProjectDetailView.as_view(), name='projects_project'),
# )