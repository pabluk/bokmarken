from django.db import models
from django.contrib.auth.models import User


class Linkshelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField('created at')
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Link(models.Model):
    url = models.URLField(max_length=1024)
    created_at = models.DateTimeField('created at')
    linkshelf = models.ForeignKey(Linkshelf)

    def __unicode__(self):
        return self.url
