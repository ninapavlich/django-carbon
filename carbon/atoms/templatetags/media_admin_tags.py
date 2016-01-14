from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Library

try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

register = Library()





@register.assignment_tag(takes_context=True)
def get_document_folder_add_url(context, current_folder = None):
  image_model = settings.DOCUMENT_FOLDER_MODEL.split('.')
  app_label = image_model[0]
  model_name = image_model[1]
  
  url = reverse('admin:%s_%s_add'%(app_label.lower(), model_name.lower()))  

  if current_folder:
    request = context['request']
    current_url = request.get_full_path()
    url = '%s?%s'%(url, urlencode({'parent': current_folder.pk, '_redirect_to':current_url}))

  return url


@register.assignment_tag(takes_context=True)
def get_changelist_url(context, model_admin):
    return reverse('admin:%s_%s_changelist'%(model_admin.model._meta.app_label.lower(), model_admin.model._meta.object_name.lower()))



@register.assignment_tag(takes_context=True)
def get_current_folder(context, model_name):
  image_model = model_name.split('.')
  app_label = image_model[0]
  model_name = image_model[1]
  model = get_model(app_label, model_name)

  request = context.get('request')
  folder_id = request.GET.get("folder__id__exact", None)

  if folder_id is None:
    return None
  else:
    try:
      return model._default_manager.get(id=folder_id)
    except:
      return None

@register.assignment_tag(takes_context=True)
def get_child_folders(context, model_name):
  image_model = model_name.split('.')
  app_label = image_model[0]
  model_name = image_model[1]
  model = get_model(app_label, model_name)

  request = context.get('request')
  folder_id = request.GET.get("folder__id__exact", None)

  if folder_id is None:
    return model._default_manager.filter(parent=None)
  else:
    return model._default_manager.filter(parent__id=folder_id)
