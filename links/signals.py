from django.dispatch import receiver
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from tastypie.models import create_api_key

from links.models import Linkshelf


@receiver(post_save, sender=User, dispatch_uid='create_default_linkshelf')
def create_default_linkshelf(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    if created:
        name = instance.email.split('@')[0]
        Linkshelf.objects.create(name=name, user=instance)


post_save.connect(create_api_key, sender=User)
