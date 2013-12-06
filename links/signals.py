from django.db.models.signals import post_save
from django.contrib.auth.models import User

from tastypie.models import create_api_key


post_save.connect(create_api_key, sender=User)
