from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from links.models import Link


class LinkTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test@example.com', 'test_pass')

    def test_domain(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, auto_update=False, user=self.user)
        self.assertEqual(link.domain(), 'www.python.org')

    def test_domain_complete_url(self):
        url = 'http://www.example.com:8080/path1/path2?queryparams=value#hashfragment'
        link = Link.objects.create(url=url, auto_update=False, user=self.user)
        self.assertEqual(link.domain(), 'www.example.com')

    def test_simple_url(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, auto_update=False, user=self.user)
        self.assertEqual(link.simple_url(), 'www.python.org/about/')

    def test_simple_url_domain_end_slash(self):
        url = 'http://www.python.org/'
        link = Link.objects.create(url=url, auto_update=False, user=self.user)
        self.assertEqual(link.simple_url(), 'www.python.org')

    def test_simple_url_domain_complete_url(self):
        url = 'http://example.com:8080/path?q=v#frag'
        link = Link.objects.create(url=url, auto_update=False, user=self.user)
        self.assertEqual(link.simple_url(), 'example.com:8080/path?q=v#frag')

    def test_default_auto_update(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, user=self.user)
        self.assertTrue(link.auto_update)
        self.assertTrue(link.is_update)

    def test_no_auto_update(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, auto_update=False, user=self.user)
        self.assertFalse(link.auto_update)
        self.assertFalse(link.is_update)

        link.auto_update = True
        link.save()
        self.assertTrue(link.is_update)


class LinkResourceTest(ResourceTestCase):
    def setUp(self):
        super(LinkResourceTest, self).setUp()
        self.user = User.objects.create_user('test_user', 'test@example.com', 'test_pass')

        url = 'http://www.python.org/'
        self.link_1 = Link.objects.create(url=url, auto_update=False, user=self.user)

        self.api_link_url = '/api/v1/link/'

    def get_credentials(self):
        username = self.user.username
        api_key = self.user.api_key.key
        return self.create_apikey(username=username, api_key=api_key)

    def test_link_list(self):
        r = self.api_client.get(self.api_link_url, format='json',
                                authentication=self.get_credentials())
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
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        self.assertEqual(Link.objects.filter(url=url).count(), 1)

    def test_link_add_default_auto_update(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
        }
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        self.assertEqual(Link.objects.filter(url=url).count(), 1)

        link = Link.objects.get(url=url)
        self.assertTrue(link.is_update)

    def test_link_add_no_auto_update(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
            'auto_update': False,
        }
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        self.assertEqual(Link.objects.filter(url=url).count(), 1)

        link = Link.objects.get(url=url)
        self.assertFalse(link.is_update)

    def test_link_add_default_public(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
        }
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
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
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        link = Link.objects.get(url=url)
        self.assertTrue(link.is_public)

    def test_link_delete(self):
        url = 'http://www.google.com/'
        post_data = {'url': url}
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertEqual(Link.objects.filter(url=url).count(), 1)
        link = Link.objects.latest('id')
        detail_url = '%s%s/' % (self.api_link_url, link.pk)
        r = self.api_client.delete(detail_url, format='json', authentication=self.get_credentials())
        self.assertHttpAccepted(r)
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

    def test_link_delete_only_owner(self):
        """Test that links can only be deleted by its owner."""
        bob = User.objects.create_user('bob', 'bob@example.com', 'bob_secret')
        alice = User.objects.create_user('alice', 'alice@example.com', 'alice_secret')

        bob_link = Link.objects.create(url='http://www.python.org/', user=bob)
        alice_link = Link.objects.create(url='http://www.python.org/', user=alice)

        alice_credentials = self.create_apikey(username=alice.username, api_key=alice.api_key.key)

        # Alice can delete alice_link
        detail_url = '%s%s/' % (self.api_link_url, alice_link.pk)
        r = self.api_client.delete(detail_url, format='json', authentication=alice_credentials)
        self.assertHttpAccepted(r)
        # Alice tries to delete bob_link
        detail_url = '%s%s/' % (self.api_link_url, bob_link.pk)
        r = self.api_client.delete(detail_url, format='json', authentication=alice_credentials)
        self.assertHttpNotFound(r)

    def test_link_update_is_public(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
            'is_public': True,
        }
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        link = Link.objects.get(url=url)
        self.assertTrue(link.is_public)

        post_data = {
            'is_public': False,
        }
        link = Link.objects.latest('id')
        detail_url = '%s%s/' % (self.api_link_url, link.pk)
        r = self.api_client.patch(detail_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpAccepted(r)
        link = Link.objects.get(url=url)
        self.assertFalse(link.is_public)

    def test_link_update_is_archived(self):
        url = 'http://www.google.com/'
        self.assertEqual(Link.objects.filter(url=url).count(), 0)

        post_data = {
            'url': url,
            'is_archived': False,
        }
        r = self.api_client.post(self.api_link_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(r)
        link = Link.objects.get(url=url)
        self.assertFalse(link.is_archived)

        post_data = {
            'is_archived': True,
        }
        link = Link.objects.get(url=url)
        detail_url = '%s%s/' % (self.api_link_url, link.pk)
        r = self.api_client.patch(detail_url, format='json',
                                 data=post_data, authentication=self.get_credentials())
        self.assertHttpAccepted(r)
        link = Link.objects.get(url=url)
        self.assertTrue(link.is_archived)
