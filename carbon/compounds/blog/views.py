from django.views.generic import DetailView
from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *
from .forms import *


class BlogArticleDetailView(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    # model = BlogArticle
    pass
    

class BlogTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = BlogTag
    pass

class BlogCategoryView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = BlogCategory
    pass    