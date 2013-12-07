from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication

from links.models import Link


class LinkResource(ModelResource):
    class Meta:
        queryset = Link.objects.all()
        resource_name = 'link'
        #excludes = ['is_updated', 'is_public']
        fields = ['url']
        allow_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        return super(LinkResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def get_object_list(self, request):
        return super(LinkResource, self).get_object_list(request).filter(user=request.user)
