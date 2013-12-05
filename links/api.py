from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication

from links.models import Link, Linkshelf


class LinkshelfResource(ModelResource):
    class Meta:
        queryset = Linkshelf.objects.all()
        resource_name = 'linkshelf'
        allowed_methods = ['get']


class LinkResource(ModelResource):
    linkshelf = fields.ForeignKey(LinkshelfResource, 'linkshelf')

    class Meta:
        queryset = Link.objects.all()
        resource_name = 'link'
        excludes = ['is_updated']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def get_object_list(self, request):
        linkshelf = request.user.linkshelf_set.latest('id')
        return super(LinkResource, self).get_object_list(request).filter(linkshelf=linkshelf)

    def aaobj_create(self, bundle, **kwargs):
        print "::", bundle.request.user
        return super(LinkResource, self).obj_create(bundle, user=bundle.request.user)

    def aaapply_authorization_limits(self, request, object_list):
        linkshelf = request.user.linkshelf_set.latest('id')
        print ">>", linkshelf
        return object_list.filter(linkshelf=linkshelf)
