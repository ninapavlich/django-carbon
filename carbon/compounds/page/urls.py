from django.conf.urls import patterns, url, include

from .views import *


urlpatterns = patterns('',
	url(r'^(?P<path>[-_\/\w]*)$', PageDetail.as_view(), name="pages_page"),
	url(r'^(?P<path>.*)$', PageDetail.as_view(), name="pages_page"),
)