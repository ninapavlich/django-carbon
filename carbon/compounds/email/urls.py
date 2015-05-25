from django.conf.urls import patterns, url, include

from .views import *

urlpatterns = patterns('',
   	
   	# url( (r'^%s/record/(?P<access_key>.*)\.jpeg$'%settings.EMAIL_DOMAIN), EmailRecordView.as_view(), name='email_record_view'),
   	# url( (r'^%s/view/(?P<access_key>.*)/$'%settings.EMAIL_DOMAIN), EmailOnlineView.as_view(), name='email_online_view'),
   	# url( (r'^%s/rendered/(?P<access_key>.*)/$'%settings.EMAIL_DOMAIN), EmailRenderedView.as_view(), name='email_rendered_view'),
   	# url( (r'^%s/settings/(?P<access_key>.*)/$'%settings.EMAIL_DOMAIN), EmailSettingsView.as_view(), name='email_settings_view'),

)