from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from links.models import Link

class LinkTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test@example.com', 'test_pass')

    def test_domain(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, is_update=True, user=self.user)
        self.assertEqual(link.domain(), 'www.python.org')

    def test_domain_complete_url(self):
        url = 'http://www.example.com:8080/path1/path2?queryparams=value#hashfragment'
        link = Link.objects.create(url=url, is_update=True, user=self.user)
        self.assertEqual(link.domain(), 'www.example.com')

    def test_simple_url(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, is_update=True, user=self.user)
        self.assertEqual(link.simple_url(), 'www.python.org/about/')

    def test_simple_url_domain_end_slash(self):
        url = 'http://www.python.org/'
        link = Link.objects.create(url=url, is_update=True, user=self.user)
        self.assertEqual(link.simple_url(), 'www.python.org')

    def test_simple_url_domain_complete_url(self):
        url = 'http://example.com:8080/path?q=v#frag'
        link = Link.objects.create(url=url, is_update=True, user=self.user)
        self.assertEqual(link.simple_url(), 'example.com:8080/path?q=v#frag')


class LinkResourceTest(ResourceTestCase):
    def setUp(self):
        super(LinkResourceTest, self).setUp()
        self.user = User.objects.create_user('test_user', 'test@example.com', 'test_pass')

        url = 'http://www.python.org/'
        self.link_1 = Link.objects.create(url=url, is_update=True, user=self.user)

        self.api_link_url = '/api/v1/link/'

    def get_credentials(self):
        username = self.user.username
        api_key = self.user.api_key.key
        return self.create_apikey(username=username, api_key=api_key)

    def test_link_list(self):
        r = self.api_client.get(self.api_link_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(r)
        self.assertEqual(len(self.deserialize(r)['objects']), 1)

    def test_link_list_unauthenticated(self):
        r = self.api_client.get(self.api_link_url, format='json')
        self.assertHttpUnauthorized(r)

    def test_link_add(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
        }
        r = self.api_client.post(self.api_link_url, format='json', data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        self.assertEqual(Link.objects.filter(url=url).count(), 1)

    def test_link_add_default_update(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
        }
        r = self.api_client.post(self.api_link_url, format='json', data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        self.assertEqual(Link.objects.filter(url=url).count(), 1)

        link = Link.objects.get(url=url)
        self.assertTrue(link.is_update)

    def test_link_add_default_public(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
        }
        r = self.api_client.post(self.api_link_url, format='json', data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        link = Link.objects.get(url=url)
        self.assertFalse(link.is_public)

    def test_link_add_set_public(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
            'is_public': True,
        }
        r = self.api_client.post(self.api_link_url, format='json', data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        link = Link.objects.get(url=url)
        self.assertTrue(link.is_public)
