from django.db.models import get_model
from django.template import Library
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings
from django.utils.safestring import mark_safe


register = Library()


@register.assignment_tag()
def get_rendered_field(field):
    if hasattr(field.field.widget, 'has_custom_render') and field.field.widget.has_custom_render==True:
        return field.field.widget.render(field)
    else:
        return field.field.widget.render(field.html_name, field.value())