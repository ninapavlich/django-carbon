from django.db.models import get_model
from django.template import Library
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.conf import settings
from django.utils.safestring import mark_safe


register = Library()


@register.assignment_tag()
def get_user_groups():

	app_label = settings.USER_GROUP_MODEL.split('.')[0]
	object_name = settings.USER_GROUP_MODEL.split('.')[1]
	model = get_model(app_label, object_name)
	return model.objects.all()