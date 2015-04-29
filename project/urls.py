from django.conf.urls import patterns, include, url
import os
ROOT_DIR = os.path.dirname(__file__)

urlpatterns = patterns('project.views',
  url(r'^$', 'index'),
  url(r'^test1$', 'test1'),
  url(r'^test2$', 'test2'),
  url(r'^bar$', 'bar'),
  url(r'^view$', 'view_project'),
)
urlpatterns += patterns('django.views.static',
  url(r'^css/(?P<path>.*)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/css')}), 
  url(r'^js/(?P<path>.*)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/js')}), 
)
