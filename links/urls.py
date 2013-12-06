from django.conf.urls import patterns, url

from links import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>\w+)/$', views.links, name='links'),
    url(r'^(?P<username>\w+)/add/$', views.add, name='add'),
)
