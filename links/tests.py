from django.test import TestCase
from django.contrib.auth.models import User

from links.models import Link, Linkshelf

class LinkTestCase(TestCase):
    def setUp(self):
        name = 'test'
        user = User.objects.create_user('test_user', 'test@example.com', 'test_pass')
        self.linkshelf = Linkshelf.objects.create(name=name, user=user)

    def test_domain(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, linkshelf=self.linkshelf)
        self.assertEqual(link.domain(), 'www.python.org')

    def test_domain_complete_url(self):
        url = 'http://www.example.com:8080/path1/path2?queryparams=value#hashfragment'
        link = Link.objects.create(url=url, linkshelf=self.linkshelf)
        self.assertEqual(link.domain(), 'www.example.com')

    def test_simple_url(self):
        url = 'http://www.python.org/about/'
        link = Link.objects.create(url=url, linkshelf=self.linkshelf)
        self.assertEqual(link.simple_url(), 'www.python.org/about/')

    def test_simple_url_domain_end_slash(self):
        url = 'http://www.python.org/'
        link = Link.objects.create(url=url, linkshelf=self.linkshelf)
        self.assertEqual(link.simple_url(), 'www.python.org')

    def test_simple_url_domain_complete_url(self):
        url = 'http://example.com:8080/path?q=v#frag'
        link = Link.objects.create(url=url, linkshelf=self.linkshelf)
        self.assertEqual(link.simple_url(), 'example.com:8080/path?q=v#frag')


