from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication

from links.models import Link


class LinkResource(ModelResource):
    class Meta:
        queryset = Link.objects.all()
        resource_name = 'link'
        excludes = ['is_updated', 'is_public']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def get_object_list(self, request):
        return super(LinkResource, self).get_object_list(request).filter(user=request.user)
