from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User

import requests
from bs4 import BeautifulSoup


class Link(models.Model):
    url = models.URLField(max_length=1024)
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    image_url = models.URLField(max_length=1024, blank=True)
    is_update = models.BooleanField(default=False, help_text=u'Current state media data.')
    auto_update = models.BooleanField(default=True, help_text=u'Fetch media data on save.')
    is_public = models.BooleanField(default=False, help_text=u'Visible on the profile page.')
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if self.auto_update:
            self.update()
        super(Link, self).save(*args, **kwargs)

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
            try:
                response = requests.get(self.url)
                if response.status_code == 200:

                    if 'image/' in response.headers['content-type']:
                        self.image_url = self.url

                    if 'text/html' in response.headers['content-type']:
                        soup = BeautifulSoup(response.text, "lxml")
                        self.title = soup.title.string.encode('utf-8').strip()

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
                            self.image_url = image_url
            except requests.exceptions.RequestException:
                # Ignore error on requests
                pass
            self.is_update = True

        return self.is_update
