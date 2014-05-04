# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django.http
import django.template

from django.utils.cache import patch_vary_headers
from .utils import get_donottrack


# http://wtanaka.com/django/django403
class Django403Middleware(object):
  """Replaces vanilla django.http.HttpResponseForbidden() responses
  with a rendering of 403.html
  """
  def process_response(self, request, response):
    # If the response object is a vanilla 403 constructed with
    # django.http.HttpResponseForbidden() then call our custom 403 view
    # function
    if isinstance(response, django.http.HttpResponseForbidden) and \
        set(dir(response)) == set(dir(django.http.HttpResponseForbidden())):
      import views
      try:
        return views.access_denied(request)
      except django.template.TemplateDoesNotExist, e:
        return views.fallback_403(request)

    return response



#https://pypi.python.org/pypi/django-donottrack/0.1
class DoNotTrackMiddleware(object):
    """
    Middleware that inspects the ``HTTP_DNT`` header and provides information
    for your app to act appropriately.

    """

    def process_request(self, request):
        """
        Inspects the request for the ``HTTP_DNT`` header and sets a
        ``donottrack`` attribute on the request object appropriately.

        Doing this here, rather than in a context processor, allows for your
        views to also take advantage of this logic.

        """
        request.donottrack = get_donottrack(request)

        return None

    def process_response(self, request, response):
        """
        Adds a vary header for ``DNT``, allowing for cache control based on the
        ``HTTP_DNT`` header.

        """
        patch_vary_headers(response, ('DNT',))

        return response
