from django.conf import settings

from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin


class PublishableView(SingleObjectMixin):



    def render_to_response(self, context, **response_kwargs):

        if self.object.is_published() == False:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': self.object._meta.verbose_name})

        return super(PublishableView, self).render_to_response(context)


class ModerationView(SingleObjectMixin):

    def render_to_response(self, context, **response_kwargs):

        if self.object.is_moderated() == False:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': self.object._meta.verbose_name})

        return super(ModerationView, self).render_to_response(context)