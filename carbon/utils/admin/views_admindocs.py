import inspect
import os
import re
from importlib import import_module

from django import template
from django.template import RequestContext
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.shortcuts import render_to_response
from django.core.exceptions import ImproperlyConfigured, ViewDoesNotExist
from django.http import Http404
from django.core import urlresolvers
from django.contrib.admindocs import utils
from django.contrib.sites.models import Site
from django.utils._os import upath
from django.utils import six
from django.utils.translation import ugettext as _

# Exclude methods starting with these strings from documentation
MODEL_METHODS_EXCLUDE = ('_', 'add_', 'delete', 'save', 'set_')

class GenericSite(object):
    domain = 'example.com'
    name = 'my site'


@staff_member_required
def custom_model_detail(request, app_label, model_name):
    if not utils.docutils_is_available:
        return missing_docutils_page(request)

    # Get the model class.
    try:
        app_mod = models.get_app(app_label)
    except ImproperlyConfigured:
        raise Http404(_("App %r not found") % app_label)
    model = None
    for m in models.get_models(app_mod):
        if m._meta.model_name == model_name:
            model = m
            break
    if model is None:
        raise Http404(_("Model %(model_name)r not found in app %(app_label)r") % {'model_name': model_name, 'app_label': app_label})

    opts = model._meta

    # Gather fields/field descriptions.
    fields = []
    fk_fields = []
    # field_hash = {}
    for field in opts.fields:
        # ForeignKey is a special case since the field will actually be a
        # descriptor that returns the other object
        if isinstance(field, models.ForeignKey):
            data_type = field.rel.to.__name__
            app_label = field.rel.to._meta.app_label
            verbose = utils.parse_rst((_("the related `%(app_label)s.%(data_type)s` object")  % {'app_label': app_label, 'data_type': data_type}), 'model', _('model:') + data_type)
            fk_fields.append(field.name)
        else:
            data_type = get_readable_field_data_type(field)
            verbose = field.verbose_name

        # field_hash[field.name] = field

        is_meta = field.name.startswith('_')

        if is_meta==False:
            fields.append({
                'name': field.name,
                'data_type': data_type,
                'verbose': verbose,
                'help_text': field.help_text,
            })

    m2m_fields = []
    # Gather many-to-many fields.
    for field in opts.many_to_many:
        data_type = field.rel.to.__name__
        app_label = field.rel.to._meta.app_label

        verbose_all = _("%(verbose_name)s. All related `%(app_label)s.%(object_name)s` objects") % {'verbose_name':field.verbose_name, 'app_label': app_label, 'object_name': data_type}
        verbose_count = _("Number of related `%(app_label)s.%(object_name)s` objects") % {'app_label': app_label, 'object_name': data_type}
        
        #verbose_all = utils.parse_rst(_("%s%s"%(verbose_description, verbose)) , 'model', _('model:') + opts.model_name),

        fields.append({
            'name': "%s.all" % field.name,
            "data_type": 'List',
            'verbose': utils.parse_rst(verbose_all , 'model', _('model:') + opts.model_name),
        })
        fields.append({
            'name'      : "%s.count" % field.name,
            'data_type' : 'Integer',
            'verbose'   : utils.parse_rst(verbose_count , 'model', _('model:') + opts.model_name),
        })
        m2m_fields.append(field.name)
        

    # Gather related objects
    for rel in opts.get_all_related_objects() + opts.get_all_related_many_to_many_objects():
        verbose = _("related `%(app_label)s.%(object_name)s` objects") % {'app_label': rel.opts.app_label, 'object_name': rel.opts.object_name}
        accessor = rel.get_accessor_name()
        fields.append({
            'name'      : "%s.all" % accessor,
            'data_type' : 'List',
            'verbose'   : utils.parse_rst(_("All %s") % verbose , 'model', _('model:') + opts.model_name),
        })
        fields.append({
            'name'      : "%s.count" % accessor,
            'data_type' : 'Integer',
            'verbose'   : utils.parse_rst(_("Number of %s") % verbose , 'model', _('model:') + opts.model_name),
        })
        m2m_fields.append(accessor)
        

    # Gather model methods.
    for func_name, func in model.__dict__.items():
        
        if (inspect.isfunction(func) and len(inspect.getargspec(func)[0]) == 1):
            try:
                for exclude in MODEL_METHODS_EXCLUDE:
                    if func_name.startswith(exclude):
                        raise StopIteration
            except StopIteration:
                continue
            verbose = func.__doc__
            if verbose:
                verbose = utils.parse_rst(utils.trim_docstring(verbose), 'model', _('model:') + opts.model_name)
            else:
                verbose = ''
            
            data_type = get_return_data_type(func_name).strip()
            if data_type == '':
                data_type = 'Function'

            fields.append({
                'name': func_name,
                'data_type': data_type,
                'verbose': verbose,
            })
        else:
            
            verbose = func.__doc__

            ignore_list = ['DoesNotExist', 'MultipleObjectsReturned', 'objects', 'unique_together', ]

            is_fk = func_name in fk_fields
            is_m2m = func_name in m2m_fields
            is_set = func_name.endswith('_set')
            is_display = func_name.endswith('_display')
            is_uppercase = func_name.isupper()
            is_meta = func_name.startswith('_')
            is_ignore = func_name in ignore_list
            is_static_method = False if not verbose else 'staticmethod' in verbose.lower()

            add_item = is_fk == False \
                and is_set == False \
                and is_display == False \
                and is_uppercase == False \
                and is_meta == False \
                and is_ignore == False \
                and is_m2m == False \
                and is_static_method == False

            if add_item:
                
                if verbose:
                    verbose = utils.parse_rst(utils.trim_docstring(verbose), 'model', _('model:') + opts.model_name)
                else:
                    verbose = ''
                data_type = get_return_data_type(func_name).strip()
                if data_type == '':
                    data_type = 'Property'
            
                fields.append({
                    'name': func_name,
                    'data_type': data_type,
                    'verbose': verbose,                    
                })


    
    return render_to_response('admin_doc/model_detail.html', {
        'root_path': urlresolvers.reverse('admin:index'),
        'name': '%s.%s' % (opts.app_label, opts.object_name),
        # Translators: %s is an object type name
        'summary': _("Attributes on %s objects") % opts.object_name,
        'description': utils.parse_rst(model.__doc__ , 'model', _('model:') + opts.model_name),
        'fields': fields,
    }, context_instance=RequestContext(request))


####################
# Helper functions #
####################

def missing_docutils_page(request):
    """Display an error message for people without docutils"""
    return render_to_response('admin_doc/missing_docutils.html')

def get_return_data_type(func_name):
    """Return a somewhat-helpful data type given a function name"""
    if func_name.startswith('get_'):
        if func_name.endswith('_list'):
            return 'List'
        elif func_name.endswith('_count'):
            return 'Integer'
    return ''

def get_readable_field_data_type(field):
    """Returns the description for a given field type, if it exists,
    Fields' descriptions can contain format strings, which will be interpolated
    against the values of field.__dict__ before being output."""

    return field.description % field.__dict__


named_group_matcher = re.compile(r'\(\?P(<\w+>).+?\)')
non_named_group_matcher = re.compile(r'\(.*?\)')
