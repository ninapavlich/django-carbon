from django.db.models import get_model
from django.template import Library
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings
from django.utils.safestring import mark_safe

from ..models import *

register = Library()


@register.assignment_tag()
def get_link_descendants(slug):
    """
    This tag gets the children and (if they're there) grandchildren of a link item.
    """

    output = []
    app_label = settings.MENU_MODEL.split('.')[0]
    object_name = settings.MENU_MODEL.split('.')[1]
    model = get_model(app_label, object_name)
    try:
        item = model.objects.get(slug=slug)
    except:
        item = None

    children = model.objects.filter(parent__slug=slug).order_by('order')
    children = [child for child in children if child.is_published()]

    descendants = {
        'item':item,
        'children':output
    }
    for child in children:
        output.append({
            'item':child,
            'children':get_link_descendants(child.slug)
        })

    return descendants

@register.assignment_tag()
def get_edit_url(object):
    if object:
        try:
            return object.edit_item_url
        except:
            pass
    return None

@register.filter(is_safe=True)
def edit_attribute(object):

    if object:
        try:
            return mark_safe('data-edit-url="%s"'%(object.edit_item_url))
        except:
            pass
    return None



@register.assignment_tag()
def get_js_package(slug, minified=False):
    model = get_model('core', 'JSPackage')
    try:
        item = model.objects.get(slug=slug)
    except:
        item = None

    if item:
        if minified:
            return '%s?v=%s'%(item.file_minified.url, item.version)
        else:
            return '%s?v=%s'%(item.file_source.url, item.version)
    return ''

@register.assignment_tag()
def get_css_package(slug, minified=False):
    model = get_model('core', 'CSSPackage')
    try:
        item = model.objects.get(slug=slug)
    except:
        item = None

    if item:
        if minified:
            return '%s?v=%s'%(item.file_minified.url, item.version)
        else:
            return '%s?v=%s'%(item.file_source.url, item.version)
    return ''    
