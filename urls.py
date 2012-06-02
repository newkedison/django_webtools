from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os
ROOT_DIR = os.path.dirname(__file__)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webtool.views.home', name='home'),
    # url(r'^webtool/', include('webtool.foo.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^web-?log/', include('weblog.urls')),
    url(r'^files/', include('fileupload.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^css/(?P<path>.*)$','django.views.static.serve', 
     { 'document_root': os.path.join(ROOT_DIR, 'static/css')}), 
    url(r'^js/(?P<path>.*)$','django.views.static.serve', 
     { 'document_root': os.path.join(ROOT_DIR, 'static/js')}), 
    url(r'^robots.txt', 'views.robots'),
)
