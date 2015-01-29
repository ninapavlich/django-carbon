from django.conf import settings

from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin


class AccessibleView(SingleObjectMixin):


    def get_object(self, queryset=None):
        
        self.object = super(AccessibleView, self).get_object(queryset)
        
        if self.object.access_allowed(self.request) == False:
            raise PermissionDenied()

        return self.object