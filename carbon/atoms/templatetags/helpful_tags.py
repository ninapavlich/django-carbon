import re
import urllib
from unidecode import unidecode
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import Library
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags


from ..models import *

register = Library()



#HELPER FUNCTIONS:

@register.assignment_tag
def getAttribute(the_object, attribute_name):
    # Try to fetch from the object, and if it's not found return None.
    # print 'get %s from %s'%(attribute_name, the_object)

    try:
        attr = the_object[attribute_name]
    except:
        attr = getattr(the_object, attribute_name, None)
    return attr

@register.simple_tag(takes_context=True)
def url_add_query(context, **kwargs):
    request = context.get('request')

    get = request.GET.copy()
    get.update(kwargs)

    path = '%s?' % request.path
    for query, val in get.items():
        path += '%s=%s&' % (query, val)


    return path[:-1]

@register.assignment_tag(takes_context=True)
def get_query_string(context):
    request = context.get('request')

    get = request.GET.copy()
    
    path = '?'
    for query, val in get.items():
        path += '%s=%s&' % (query, val)


    return path[:-1]


@register.filter
def tostring(object):
    return str(object)

@register.filter
def slugify(value):
    return slugify(unidecode(value))

def insert_ellipse(lst, ellipse=0):
    '''Insert ellipse where it's not sequential

    An ellipse is represented by @ellipse.

    E.g.:
        [1, 2, 5] -> [1, 2, 0, 5]
        [1, 2, 4] -> [1, 2, 3, 4]

    The last example is that if only one step is missing, just add it instead
    of an ellipse.
    '''

    if len(lst) <= 1:
        return list(lst[:])
    gap = lst[1] - lst[0]
    if gap <= 1:
        return [lst[0]] + insert_ellipse(lst[1:], ellipse)
    elif gap == 2:
        return [lst[0], lst[0] + 1] + insert_ellipse(lst[1:], ellipse)
    else:
        return [lst[0], ellipse] + insert_ellipse(lst[1:], ellipse)

@register.assignment_tag
def pick_pages(num_pages, current):
    '''pick pages to display in the pager

    It's like: 1 ... (x-2) (x-1) (x) (x+1) (x+2) ... N.
    '''

    ret = []

    for p in range(current - 2, current):
        if p >= 1:
            ret.append(p)
    ret.append(current)
    for p in range(current + 1, current + 3):
        if p <= num_pages:
            ret.append(p)

    if ret[0] != 1:
        ret.insert(0, 1)
    if ret[-1] != num_pages:
        ret.append(num_pages)
    ret = insert_ellipse(ret)

    return ret


@register.assignment_tag()
def url_to_edit_object(object):
    try:
        object_type = type(object).__name__
        if object_type == 'SearchResult':
            object = object.object
        
        url = reverse('admin:%s_%s_change' %(object._meta.app_label,  object._meta.model_name),  args=[object.id] )
        return url
    except:
        return None

@register.assignment_tag()
def get_model_label(object):
    try:
        object_type = type(object).__name__
        object_label = object.__unicode__()

        if object_type == 'SearchResult':
            object = object.object
            object_type = type(object).__name__
            object_label = object.__unicode__()

        return "%s %s"%(object_type.upper(), object_label)
        
    except:
        return None        




def is_path_encrypted(path):
    try:
        for SSL_PATH in settings.SSL_PATHS:
            pattern = re.compile(SSL_PATH)
            match = pattern.match(path)
            if match:
                #print 'Matched %s to pattern %s'%(path, SSL_PATH)
                return True
    except:
        return False



@register.assignment_tag(takes_context=True)
def get_canonical_url(context):

    try:
        request = context['request']
    except:
        #No request
        return None
        
    current_site = Site.objects.get_current()
    path = request.get_full_path()

    encrypt_path = is_path_encrypted(path)

    if encrypt_path:
        url  = 'https://%s%s'%(current_site.domain, path)
    else:
        url  = 'http://%s%s'%(current_site.domain, path)

    return url


@register.assignment_tag(takes_context=True)
def get_site_url(context):
    try:
        request = context['request']
    except:
        #No request
        return None
        
    request = context['request']
    full_path = ('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST'])
    domain = ''.join(full_path)
    
    return domain

@register.filter
def data_verbose(boundField):
    if boundField:
        value = boundField.value()
        field = boundField.field    
        return hasattr(field, 'choices') and dict(field.choices).get(value,'') or value
    return None

@register.assignment_tag()
def get_sorted(list, attribute, reverse=False):
    return sorted(list, key=lambda x: getattr(x, attribute), reverse=reverse)