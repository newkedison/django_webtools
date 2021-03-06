from django.conf.urls import patterns, include, url
import os
ROOT_DIR = os.path.dirname(__file__)

urlpatterns = patterns('fileupload.views',
  url(r'^(index/)?$', 'index'),
  url(r'^upload/$', 'upload'),
  url(r'^success/$', 'success'),
  url(r'^failed/$', 'failed'),
  url(r'^list/((?P<dir>[^/]+)/)?$', 'list_dir'),
  url(r'^(?P<method>get|view)/(?P<dir>[^/]+)/(?P<filename>.+)$', 'download'),
  url(r'^delete/(?P<dir>[^/]+)/(?P<file_id>.+)/$', 'delete'),
  url(r'^discuss/$', 'discuss'),
  url(r'^check/', 'check'),
)

urlpatterns += patterns('django.views.static',
  url(r'^css/(?P<path>.+)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/css')}), 
  url(r'^js/(?P<path>.+)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/js')}), 
)
