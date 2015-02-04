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
def get_link_descendants(txtid):
    """
    This tag gets the children and (if they're there) grandchildren of a link item.
    """

    output = []
    try:
        children = LinkItem.objects.filter(parent__txtid=txtid)\
            .exclude(hide=True).order_by('order')
        for child in children:
            output.append({
                'item':child,
                'children':get_link_descendants(child.txtid)
            })
    except:
        return None

    return output




@register.assignment_tag()
def get_link_set_by_txtid(txtid):

    try:
        link_sets = LinkSet.objects.filter(txtid=txtid)
        link_set = link_sets[0]
        links = LinkItem.objects.filter(parent=txtid).order_by('order')
    except:
        link_set = None
        links = None


    return {
        'set':link_set,
        'items': links
    }