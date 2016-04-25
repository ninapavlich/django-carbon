try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save



app_label = settings.CSS_RESOURCE_MODEL.split('.')[0]
object_name = settings.CSS_RESOURCE_MODEL.split('.')[1]
css_package_model = get_model(app_label, object_name)

app_label = settings.JS_RESOURCE_MODEL.split('.')[0]
object_name = settings.JS_RESOURCE_MODEL.split('.')[1]
js_package_model = get_model(app_label, object_name)

@receiver(pre_delete, sender=css_package_model, dispatch_uid='css_package_delete_signal')
def delete_css_resource(sender, instance, using, **kwargs): 
    instance.delete_downloaded_files()
    if instance.parent:
        instance.parent.request_render()

@receiver(pre_delete, sender=js_package_model, dispatch_uid='js_package_delete_signal')
def delete_js_resource(sender, instance, using, **kwargs):
    instance.delete_downloaded_files()
    if instance.parent:
        instance.parent.request_render()


@receiver(post_save, sender=css_package_model, dispatch_uid='css_package_save_signal')
def save_css_resource(sender, instance, created, **kwargs):
    if created:
        if instance.parent:
            instance.parent.request_render()

@receiver(post_save, sender=js_package_model, dispatch_uid='js_package_save_signal')
def save_js_resource(sender, instance, created, **kwargs):
    if created:
        if instance.parent:
            instance.parent.request_render()
 