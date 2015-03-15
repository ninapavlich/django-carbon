from django.db.models import get_model
from django.template import Library
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model


register = Library()


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
