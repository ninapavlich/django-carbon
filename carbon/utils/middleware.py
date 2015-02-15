# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django.http
import django.template
from django.conf import settings

from django.utils.cache import patch_vary_headers

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
        return fallback_403(request)

    return response

def fallback_403(request):
  """
  Fallback 403 handler which prints out a hard-coded string patterned
  after the Apache default 403 page.

  Templates: None
  Context: None
  """
  return django.http.HttpResponseForbidden(
      django.utils.translation.gettext(
          """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access %(path)s on this server.</p>
<hr>
</body></html>""") % {'path': request.path})

def access_denied(request, template_name='403.html'):
  """
  Default 403 handler, which looks for the  which prints out a hard-coded string patterned
  after the Apache default 403 page.

  Templates: `403.html`
  Context:
      request
          The django request object
  """
  t = django.template.loader.get_template(template_name)
  template_values = {}
  template_values['request'] = request
  return django.http.HttpResponseForbidden(
      t.render(django.template.RequestContext(request, template_values)))



#https://pypi.python.org/pypi/django-donottrack/0.1
def get_donottrack(request):
    """
    Returns ``True`` if ``HTTP_DNT`` header is ``'1'``, ``False`` otherwise.

    """
    return request.META.get('HTTP_DNT') == '1'

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

class SiteMiddlewear(object):
    def process_request(self, request):
        try:

            request.site = Site.objects.get_current()
        except:
            request.site = {
                'domain': '',
                'name': settings.GRAPPELLI_ADMIN_TITLE,
            }



class CustomSettingsMiddlewear(object):
    def process_request(self, request):

        try:

            all_settings = settings.CUSTOM_SETTINGS
            for setting in all_settings:
                if hasattr(settings, setting):
                    value = getattr(settings, setting)
                    setattr(request, setting, value)
                    #print "Added %s to request %s"%(setting, getattr(request, setting))
        except:
            pass

class ImpersonateMiddleware(object):
    def process_request(self, request):
        request.impersonating = None
        request.original_user = None
        
        if hasattr(request, 'user') and request.user and request.user.is_authenticated() and  request.user.is_superuser and "__impersonate" in request.GET:
            request.session['impersonate_id'] = int(request.GET["__impersonate"])
        elif "__unimpersonate" in request.GET:
            if "impersonate_id" in request.session:
                del request.session['impersonate_id']

            if '__unimpersonate' in request.GET:
                new_query = request.GET.copy()
                del new_query['__unimpersonate']
                new_path = "%s?%s"%(request.path, new_query.urlencode())
                return HttpResponseRedirect(new_path)
        
        if hasattr(request, 'user') and request.user and request.user.is_authenticated() and request.user.is_superuser and 'impersonate_id' in request.session:
            try:
                UserModel = get_user_model()
                user = UserModel._default_manager.get(pk=request.session['impersonate_id'])
                request.original_user = request.user
                request.impersonating = request.user = user   
                

                if '__impersonate' in request.GET:
                    new_query = request.GET.copy()
                    del new_query['__impersonate']
                    new_path = "%s?%s"%(request.path, new_query.urlencode())
                    return HttpResponseRedirect(new_path)


            except:
                pass


class AdminLoggedInCookieMiddlewear(object):
    def process_response(self, request, response):

        is_staff = hasattr(request, 'user') and request.user and request.user.is_authenticated() and request.user.is_staff
        if is_staff and not request.COOKIES.get('admin_logged_in'):
            response.set_cookie("admin_logged_in", '1')
        elif not is_staff and request.COOKIES.get('admin_logged_in'):
            response.delete_cookie("admin_logged_in")
        return response
