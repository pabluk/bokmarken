from django.conf.urls import patterns, url

from links import views


urlpatterns = patterns('',
    url(r'^add/$', views.add, name='add'),
    url(r'^(?P<name>\w+)/$', views.linkshelf, name='linkshelf'),
)
