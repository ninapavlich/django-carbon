from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.db.models import get_model


class LegacyURLMiddleware(object):

    # Defined as class-level attributes to be subclassing-friendly.
    
    def process_response(self, request, response):
        # No need to check for a redirect for non-404 responses.
        if response.status_code != 404:
            return response

        try:
            full_path = request.get_full_path()
            legacy_url_model = get_model(settings.LEGACY_URL_MODEL.split('.')[0], settings.LEGACY_URL_MODEL.split('.')[1])
            all_legacy_urls = legacy_url_model.objects.all()
            legacy_url = legacy_url_model.objects.get(url=full_path)
            return HttpResponsePermanentRedirect(legacy_url.path)
        except:
            pass

        return response