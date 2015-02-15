# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings


# https://pypi.python.org/pypi/django-donottrack/0.1
def donottrack(request):
    """
    Adds ``donottrack`` to the context, which is ``True`` if the ``HTTP_DNT``
    header is ``'1'``, ``False`` otherwise.

    This context processor requires installtion of the
    ``donottrack.middleware.DoNotTrackMiddleware``.

    Note that use of this context processor is not strictly necessary. (Though
    it is quite convenient.) If you are using the
    ``django.core.context_processors.request`` context processor, you have
    access to ``{{ request.donottrack }}``.

    """
    # We could just use the ``donottrack.utils.get_donottrack`` function rather
    # than rely on the middlware, but we want to require the middleware so that
    # the VARY header is properly patched to account for DNT.
    try:
        return {'donottrack': request.donottrack}
    except AttributeError:
        raise AttributeError("'WSGIRequest' object has no attribute 'donottrack'"
            " - 'donottrack.middleware.DoNotTrackMiddleware' must be in your"
            " MIDDLEWARE_CLASSES")

def site(request):

    try:
        return {
            'site': request.site
        }
    except:
        return {
            'site': None
        }
    

def custom_settings(request):
    object = {}

    try:

        all_settings = settings.CUSTOM_SETTINGS 
        for setting in all_settings:
            if hasattr(request, setting):
                value = getattr(request, setting)
                object[setting] = value         
    except:
        pass

    return object


def impersonating(request):
    object = {}

    return {
            'impersonating': request.impersonating
        }
