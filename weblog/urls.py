from django.conf.urls.defaults import patterns, include, url
import os
ROOT_DIR = os.path.dirname(__file__)

urlpatterns = patterns('weblog.views',
  url(r'^$', 'index'),
  url(r'^index$', 'index'),
  url(r'^p/(?P<person>.*)$', 'view_person'),
  url(r'^a/(?P<action>.*)$', 'view_action'),
  url(r'^all$', 'view_all'),
  url(r'^remarks/(?P<id>\d+)$', 'view_remarks'),
  url(r'^discuss$', 'view_discuss'),
  url(r'^money$', 'view_money'),
)
urlpatterns += patterns('django.views.static',
  url(r'^css/(?P<path>.*)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/css')}), 
  url(r'^js/(?P<path>.*)$','serve', 
   { 'document_root': os.path.join(ROOT_DIR, 'static/js')}), 
)
