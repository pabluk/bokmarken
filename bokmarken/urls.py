from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

from tastypie.api import Api
from links.api import LinkResource

v1_api = Api(api_name='v1')
v1_api.register(LinkResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bokmarken.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),

    url(r'^api/$', TemplateView.as_view(template_name='api.html'), name='api'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r'^', include('links.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
