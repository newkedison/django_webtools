from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('project.views',
  url(r'^$', 'index'),
  url(r'^test1$', 'test1'),
  url(r'^test2$', 'test2'),
  url(r'^bar$', 'bar'),
  url(r'^view$', 'view_project'),
  # url(r'^webtool/', include('webtool.foo.urls')),
)
