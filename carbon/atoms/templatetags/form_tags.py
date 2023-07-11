import traceback

from django.template import Library

register = Library()


@register.assignment_tag(takes_context=True)
def get_rendered_field(context, field):

    if hasattr(field.field.widget, 'has_custom_render') and field.field.widget.has_custom_render is True:

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
