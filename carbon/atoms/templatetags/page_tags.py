from django.template import Library
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured


register = Library()


@register.assignment_tag()
def get_page_by_slug(slug=None):
   
    output = []
    app_label = settings.PAGE_MODEL.split('.')[0]
    object_name = settings.PAGE_MODEL.split('.')[1]
    model = get_model(app_label, object_name)
    
    try:
        item = model.objects.get(slug=slug)
    except:
        item = None

    return item
