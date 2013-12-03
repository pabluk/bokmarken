import os.path
from StringIO import StringIO
from urlparse import urlparse

from django.db import models
from django.core.files import File
from django.contrib.auth.models import User

import requests
from bs4 import BeautifulSoup
from PIL import Image


class Linkshelf(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Link(models.Model):
    url = models.URLField(max_length=1024)
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    image = models.ImageField(upload_to='images', max_length=512, blank=True)
    is_update = models.BooleanField(default=False)
    linkshelf = models.ForeignKey(Linkshelf)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.url

    def domain(self):
        """Extract and return the domain name from url."""
        parsed = urlparse(self.url)
        return parsed.netloc.split(':')[0]

    def simple_url(self):
        """Returns url without the protocol component."""
        protocols = ['http', 'https', 'ftp', 'file']

        simple_url = self.url
        for proto in protocols:
            schema = '%s://' % proto
            if self.url.startswith(schema):
                simple_url = self.url.replace(schema, '')

        parsed = urlparse(self.url)
        if not (parsed.params and parsed.query and parsed.fragment) and parsed.path == '/':
            if simple_url.endswith('/'):
                simple_url = simple_url[:-1]

        return simple_url

    def update(self):
        if not self.is_update:
            response = requests.get(self.url)
            if response.status_code == 200:

                if 'image/' in response.headers['content-type']:
                    response = requests.get(self.url)
                    image = StringIO(response.content)
                    self.image.save(os.path.basename(self.url), File(image))

                if 'text/html' in response.headers['content-type']:
                    soup = BeautifulSoup(response.text)
                    self.title = soup.title.string.encode('utf-8')

                    image_url = None

                    if not image_url:
                        meta_tag = soup.find('meta', {'name': 'twitter:image'})
                        if meta_tag and meta_tag.has_attr('content'):
                            image_url = meta_tag.get('content')
                        if meta_tag and meta_tag.has_attr('value'):
                            image_url = meta_tag.get('value')

                    if not image_url:
                        meta_tag = soup.find('meta', {'property': 'og:image'})
                        if meta_tag and meta_tag.has_attr('content'):
                            image_url = meta_tag.get('content')

                    if image_url:
                        response = requests.get(image_url)
                        image = StringIO(response.content)
                        self.image.save(os.path.basename(image_url), File(image))
            self.is_update = True

        return self.is_update
