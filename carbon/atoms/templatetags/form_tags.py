import sys, traceback

from django.template import Library
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

register = Library()


@register.assignment_tag(takes_context=True)
def get_rendered_field(context, field):
    
    if hasattr(field.field.widget, 'has_custom_render') and field.field.widget.has_custom_render==True:

        try:
            rendered = field.field.widget.render(field, context)            
        except Exception, err:  
            rendered = traceback.print_exc()            

        return rendered
    else:
        return field.field.widget.render(field.html_name, field.value())

@register.filter
def tostring(value):
    return str(value)        