# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

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
      
      try:
        return access_denied(request)


      except django.template.TemplateDoesNotExist, e:
        return fallback_403(request)

    return response

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
def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)


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
        if hasattr(request, 'donottrack') and request.donottrack:
          response.set_cookie("donottrack", '1')
        else:
          response.delete_cookie("donottrack")


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


class SiteVersionMiddleware(object):

    def get_heroku_release_version(self):
        try:
            import heroku
            key = settings.HEROKU_API_KEY
            cloud = heroku.from_key(key)
            app = cloud.apps[settings.HEROKU_APP_LABEL]            
            latest_release = app.releases[-1]
            return latest_release.name
        except:
            return None

    def get_git_release_version(self):
        try:
            import subprocess
            short_revision = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).replace('\n','')
            return '@%s'%(short_revision)
        except:
            return None

    def process_request(self, request):
        if hasattr(request, 'user') and request.user and request.user.is_authenticated() and request.user.is_staff: 
            if settings.IS_ON_SERVER:
                if settings.IS_ON_HEROKU:
                    setattr(request, "RELEASE_VERSION", self.get_heroku_release_version())
                else:
                    setattr(request, "RELEASE_VERSION", self.get_git_release_version())
            else:
                git_version = self.get_git_release_version()
                heroku_version = self.get_heroku_release_version()

                if git_version and heroku_version:
                    version = '%s %s'%(git_version, heroku_version)
                elif git_version:
                    version = git_version
                elif heroku_version:
                    version = heroku_version
                else:
                    version = "UNKNOWN"

                setattr(request, "RELEASE_VERSION", version)