import re
import urllib
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.html import strip_tags

from ..models import *

register = Library()


@register.assignment_tag()
def get_link_descendants(slug):
    """
    This tag gets the children and (if they're there) grandchildren of a link item.
    """

    output = []
    children = MenuItem.objects.filter(parent__slug=slug).order_by('order')
    children = [child for child in children if child.is_published()]

    for child in children:
        output.append({
            'item':child,
            'children':get_link_descendants(child.slug)
        })
    return output
