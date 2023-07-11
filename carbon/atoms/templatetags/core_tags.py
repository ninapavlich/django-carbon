from django.template import Library
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

from ..models import *

register = Library()


@register.assignment_tag()
def get_link_descendants(slug=None, item=None):
    """
    This tag gets the children and (if they're there) grandchildren of a link item.
    """
    if slug is None and item is None:
        raise ImproperlyConfigured("Either slug or item must be defined")

    output = []
    app_label = settings.MENU_MODEL.split('.')[0]
    object_name = settings.MENU_MODEL.split('.')[1]
    model = get_model(app_label, object_name)

    if not item:
        try:
            item = model.objects.get(slug=slug)
        except:
            item = None

    if slug:
        children = model.objects.filter(parent__slug=slug).order_by('order').prefetch_related('content_object')
    elif item:
        children = model.objects.filter(parent=item).order_by('order').prefetch_related('content_object')

    children = [] if item is None else [child for child in item.get_children() if child.is_published()]

    descendants = {
        'item': item,
        'children': output
    }
    for child in children:
        output.append({
            'item': child,
            'children': get_link_descendants(None, child)
        })

    return descendants


@register.assignment_tag(takes_context=True)
def get_edit_url(context, object):
    request = context['request']
    if request.user and request.user.is_authenticated() and request.user.is_staff:
        if object:
            try:
                return object.edit_item_url
            except:
                pass
        return None
    return None


@register.assignment_tag(takes_context=True)
def get_object_cache_key(context, object, extra_cache_context=None):

    try:
        # Store a unique key for the object app, model and ID
        object_key = u'%s.%s.%s' % (object.__class__._meta.app_label, object.__class__._meta.model_name, object.pk)

        if not extra_cache_context:
            extra_cache_context = ''

        # Combine this key with the last modified date
        modified_date = '' if not hasattr(object, "modified_date") else object.modified_date

        key = u'%s:%s:%s' % (object_key, extra_cache_context, modified_date)
        return key
    except:
        return str(object)


# TODO -- figure out a way to make this check if user is admin before returning url
@register.filter(is_safe=True)
def edit_attribute(object):
    if object:
        try:
            return mark_safe('data-edit-url="%s"' % (object.edit_item_url))
        except:
            pass
    return None


@register.assignment_tag()
def get_js_package(slug, minified=False):
    model = get_model('core', 'JSPackage')
    try:
        item = model.objects.defer("generated_file_minified", "generated_file_source").get(slug=slug)

    except:
        item = None

    if item:
        return item.get_url(minified)
    return ''


@register.assignment_tag()
def get_js_source(slug, minified=False):
    model = get_model('core', 'JSPackage')
    try:
        item = model.objects.only("generated_file_source", "generated_file_minified").get(slug=slug)
    except:
        item = None

    if item:
        if minified:
            return item.generated_file_minified
        else:
            return item.generated_file_source
    return ''


@register.assignment_tag()
def get_css_package(slug, minified=False):
    model = get_model('core', 'CSSPackage')
    try:
        item = model.objects.defer("generated_file_minified", "generated_file_source").get(slug=slug)
    except:
        item = None

    if item:
        return item.get_url(minified)
    return ''


@register.assignment_tag()
def get_css_source(slug, minified=False):
    model = get_model('core', 'CSSPackage')
    try:
        item = model.objects.only("generated_file_minified", "generated_file_source").get(slug=slug)
    except:
        item = None

    if item:
        if minified:
            return item.generated_file_minified
        else:
            return item.generated_file_source
    return ''
