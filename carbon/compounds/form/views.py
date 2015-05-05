from __future__ import unicode_literals

import json

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.http import urlquote
from django.views.generic.base import TemplateView
from email_extras.utils import send_mail_template

from forms_builder.forms.forms import FormForForm
from forms_builder.forms.models import Form
from forms_builder.forms.settings import EMAIL_FAIL_SILENTLY
from forms_builder.forms.signals import form_invalid, form_valid
from forms_builder.forms.utils import split_choices


class FormDetailView(PublishableView, AddressibleView, DetailView):

    def get_form(self):
        pass #TODO

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        return super(FormDetail, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = self.get_form()
        if self.form.is_valid():
            
            if self.object.redirect_url_on_submission:
                return HttpResponseRedirect(self.object.redirect_url_on_submission)
            else:
                #TODO: REnder thank you...
                pass

        return super(FormDetail, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormDetail, self).get_context_data(**kwargs)
            
        context['form'] = self.form

        return context