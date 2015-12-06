from django.conf import settings
from django.template import Library, Context, Template, TemplateSyntaxError, Variable, Node
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

register = Library()


@register.assignment_tag(takes_context=True)
def get_email_category_by_id(context, id):

    app_label = settings.EMAIL_CATEGORY_MODEL.split('.')[0]
    object_name = settings.EMAIL_CATEGORY_MODEL.split('.')[1]
    model = get_model(app_label, object_name)
    try:
        return model.objects.get(pk=id)
    except:
        return None