from django.views.generic import DetailView, ListView
from django.db.models.loading import get_model
from django.conf import settings

from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *
from .forms import *

class BaseBlogView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(BaseBlogView, self).get_context_data(**kwargs)
            
        tag_model = get_model(settings.BLOG_TAG_MODEL.split('.')[0], settings.BLOG_TAG_MODEL.split('.')[1])
        category_model = get_model(settings.BLOG_CATEGORY_MODEL.split('.')[0], settings.BLOG_CATEGORY_MODEL.split('.')[1])
        #article_model = get_model(settings.BLOG_ARTICLE_MODEL.split('.')[0], settings.BLOG_ARTICLE_MODEL.split('.')[1])
        
        context['tags'] = tag_model.objects.published()
        context['categories'] = category_model.objects.published()

        return context


class BlogArticleDetailView(NonAdminCachableView, PublishableView, AddressibleView, BaseBlogView):

    # model = BlogArticle
    pass
    
class BlogTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogView):

    # model = BlogTag
    pass

class BlogCategoryView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogView):

    # model = BlogCategory
    pass

class BlogRollView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogView):

    # model = Page

    # def get_children(self):
    # articles = BlogArticle.objects.published()
    # return [article for article in articles if article.is_published()]
    pass
    

class BlogTagListView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogView):

    # model = Page
    # def get_children(self):
    # articles = BlogTag.objects.published()
    # return [article for article in articles if article.is_published()]
    pass     