from django.views.generic import DetailView, ListView
from django.db.models.loading import get_model
from django.conf import settings

from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *
from .forms import *


class BaseBlogDeatilView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(BaseBlogDeatilView, self).get_context_data(**kwargs)
            
        print 'todo: Get next/previous, and current tag'
        
        context['next'] = None
        context['previous'] = None

        return context

class BaseBlogListView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(BaseBlogListView, self).get_context_data(**kwargs)
            
        tag_model = get_model(settings.BLOG_TAG_MODEL.split('.')[0], settings.BLOG_TAG_MODEL.split('.')[1])
        category_model = get_model(settings.BLOG_CATEGORY_MODEL.split('.')[0], settings.BLOG_CATEGORY_MODEL.split('.')[1])
        #article_model = get_model(settings.BLOG_ARTICLE_MODEL.split('.')[0], settings.BLOG_ARTICLE_MODEL.split('.')[1])
        
        context['tags'] = tag_model.objects.published()
        context['categories'] = category_model.objects.published()

        return context


class BlogArticleDetailView(NonAdminCachableView, PublishableView, AddressibleView, BaseBlogDeatilView):


    # model = BlogArticle
    def get_object_query(self, queryset, path):
        return queryset.filter(path=path).select_related('template', 'category').prefetch_related('tags', 'related').get()

    
class BlogTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = BlogTag
    pass

class BlogCategoryView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = BlogCategory
    pass

class BlogRollView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = Page

    # def get_children(self):
    # articles = BlogArticle.objects.published()
    # return [article for article in articles if article.is_published()]
    pass
    

class BlogTagListView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = Page
    # def get_children(self):
    # articles = BlogTag.objects.published()
    # return [article for article in articles if article.is_published()]
    pass     

class BlogContributorListView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = settings.BLOG_ROLE_USER_MODEL
    # def get_children(self):
    # articles = BlogTag.objects.published()
    # return [article for article in articles if article.is_published()]
    pass  

class BlogContributorDetailView(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    # model = settings.BLOG_ROLE_USER_MODEL
    # def get_children(self):
    # articles = BlogTag.objects.published()
    # return [article for article in articles if article.is_published()]
    pass  