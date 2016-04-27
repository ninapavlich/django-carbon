from django.conf import settings

from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import SingleObjectMixin


class PublishableView(SingleObjectMixin):

    def is_published(self):
        if not self.object:
            self.object = self.get_object()
        if not self.object:
            return False

        if self.object.is_published() == False:
            is_super_user = hasattr(self.request, 'user') and self.request.user and self.request.user.is_authenticated() and self.request.user.is_superuser
            if is_super_user==False:
                return False
        else:
            return True


    def get(self, request, *args, **kwargs):
        if self.is_published() == False:
            raise Http404(_("No published %(verbose_name)s found matching the query") %
                        {'verbose_name': self.model._meta.verbose_name})

        return super(PublishableView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if self.is_published() == False:
            raise Http404(_("No published %(verbose_name)s found matching the query") %
                        {'verbose_name': self.model._meta.verbose_name})

        return super(PublishableView, self).post(request, *args, **kwargs)



class ModerationView(SingleObjectMixin):

    def is_moderated(self):
        if not self.object:
            self.object = self.get_object()
        if not self.object:
            return False
        if self.object.is_moderated() == False:
            is_super_user = hasattr(self.request, 'user') and self.request.user and self.request.user.is_authenticated() and self.request.user.is_superuser
            if is_super_user==False:
                return False
        else:
            return True


    def get(self, request, *args, **kwargs):
        if self.is_moderated() == False:
            raise Http404(_("No moderated %(verbose_name)s found matching the query") %
                        {'verbose_name': self.model._meta.verbose_name})

        return super(ModerationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if self.is_moderated() == False:
            raise Http404(_("No moderated %(verbose_name)s found matching the query") %
                        {'verbose_name': self.model._meta.verbose_name})

        return super(ModerationView, self).post(request, *args, **kwargs)
