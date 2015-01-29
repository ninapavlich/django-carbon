from django.views.generic import DetailView
from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *


class ProjectDetailView(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    model = Project



class ProjectCategoryView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    model = ProjectCategory