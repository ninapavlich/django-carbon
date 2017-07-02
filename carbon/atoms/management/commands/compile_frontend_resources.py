from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site


try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model


app_label = settings.CSS_PACKAGE_MODEL.split('.')[0]
object_name = settings.CSS_PACKAGE_MODEL.split('.')[1]
css_package_model = get_model(app_label, object_name)

app_label = settings.JS_PACKAGE_MODEL.split('.')[0]
object_name = settings.JS_PACKAGE_MODEL.split('.')[1]
js_package_model = get_model(app_label, object_name)


class Command(BaseCommand):
    args = ''
    help = ''

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='type[.PrimaryKey]', nargs='*',
            help='Compile a specific resource using format <type>.<pk> - For example: css.1 or js.99',
        )
        

    def handle(self, *app_labels, **options):
        update_list = []

        if len(app_labels) == 0:
            css_packages = css_package_model.objects.filter(needs_render=True)
            update_list += list(css_packages)

            js_packages = js_package_model.objects.filter(needs_render=True)
            update_list += list(js_packages)

        else:

            for label in app_labels:
                try:
                    model_type, item_pk = label.split('.')
                    
                    if model_type == 'css':

                        css_package = css_package_model.objects.get(pk=item_pk)
                        update_list.append(css_package)

                    elif model_type == 'js':

                        js_package = js_package_model.objects.get(pk=item_pk)
                        update_list.append(js_package)

                except:
                    print "Error parsing %s. Use format <type>.<pk> - For example: css.1 or js.99"

        if len(update_list) > 0;
            if settings.DEBUG:
                print u'Going to  updates %s resources'%(len(update_list))
            for item in update_list:
                if settings.DEBUG:
                    print u"-- Rendering %s"%(item)
                item.render()
                if settings.DEBUG:
                    print u"-- Rendering complete."
        else:
            if settings.DEBUG:
                print u'Nothing to compile'
                
