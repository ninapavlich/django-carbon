from django.db.models import get_model
from django.template import Library
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings
from django.utils.safestring import mark_safe


register = Library()


@register.assignment_tag(takes_context=True)
def get_rendered_field(context, field):
	
	if hasattr(field.field.widget, 'has_custom_render') and field.field.widget.has_custom_render==True:
		rendered = field.field.widget.render(field, context)
		return rendered
	else:
		return field.field.widget.render(field.html_name, field.value())

@register.filter
def tostring(value):
	return str(value)        