from django.db.models import get_model
from django.template import Library
from django.core.urlresolvers import reverse

from ..models import *

register = Library()


@register.assignment_tag()
def get_variant_url(object, variant_name):
    return object.get_variant_url(variant_name)

@register.assignment_tag()
def get_variant_width(object, variant_name):
    return object.get_variant_width(variant_name)

@register.assignment_tag()
def get_variant_height(object, variant_name):
    return object.get_variant_height(variant_name)


@register.filter
def filename(full_path):
    head, tail = os.path.split(full_path)
    return tail