from django import template
from libgravatar import Gravatar

register = template.Library()


@register.filter
def gravatar_url(value):
    g = Gravatar(value)
    return g.get_image(size=72)
