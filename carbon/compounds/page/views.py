from django.views.generic import DetailView
from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *


class PageDetail(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    # model = Page
    pass
    



class PageTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = PageTag
    pass