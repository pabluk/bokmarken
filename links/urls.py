from django.conf.urls import patterns, url

from links import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^archive/$', views.archive, name='archive'),

    # Must be the latest url
    url(r'^(?P<username>\w+)/$', views.public, name='public'),
)
