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
def get_tags(slug):
    pass

@register.assignment_tag()
def get_categories(slug):
    pass

@register.assignment_tag()
def get_blog_posts(slug):
    pass