from django.views.generic import DetailView
from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *

from .templates import CustomTemplateResponse
#from django.template.response import TemplateResponse

class PageDetail(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    model = Page

    



class PageTagView(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    model = PageTag