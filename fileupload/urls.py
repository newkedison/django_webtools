from django.conf.urls.defaults import patterns, include, url
import os
ROOT_DIR = os.path.dirname(__file__)

urlpatterns = patterns('fileupload.views',
  url(r'^(index)?$', 'index'),
  url(r'^upload$', 'upload'),
  url(r'^success$', 'success'),
  url(r'^get/(?P<prefix>[^/]+)/(?P<filename>.*)$', 'index'),
)

urlpatterns += patterns('django.views.static',
  url(r'^css/(?P<path>.*)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/css')}), 
  url(r'^js/(?P<path>.*)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/js')}), 
)
