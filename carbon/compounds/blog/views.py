from django.views.generic import DetailView, ListView
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

class BlogRollView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = Page

    # def get_children(self):
    # articles = BlogArticle.objects.published()
    # return [article for article in articles if article.is_published()]
    pass

class BlogTagListView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = Page
    # def get_children(self):
    # articles = BlogTag.objects.published()
    # return [article for article in articles if article.is_published()]
    pass     