from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from links.api import LinkResource, LinkshelfResource

v1_api = Api(api_name='v1')
v1_api.register(LinkResource())
v1_api.register(LinkshelfResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bokmarken.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('links.urls')),
    url(r'^api/', include(v1_api.urls)),

    (r'', include('django_browserid.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
