from django.views.generic import DetailView, ListView
from django.conf import settings
from django.views.generic.edit import FormMixin, ProcessFormView
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model


from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *
from .forms import *

class BlogCommentMixin(FormMixin, ProcessFormView):

    form_class = BlogCommentForm
    was_posted = False


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.was_posted = False
        if self.object.allow_comments:
            form = self.get_form()        
        else:
            form = None

        context = self.get_context_data(object=self.object,form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.was_posted = True
        
        if self.object.allow_comments:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.get(*args, **kwargs)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


    def get_form_kwargs( self ):
        kwargs = super( BlogCommentMixin, self ).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['was_posted'] = self.was_posted
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.save()
        return super(BlogCommentMixin, self).form_valid(form)

class BaseBlogDetailView(BlogCommentMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseBlogDetailView, self).get_context_data(**kwargs)
            
        # print 'todo: Get next/previous, and current tag'
        
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


class BlogArticleDetailView(NonAdminCachableView, PublishableView, AddressibleView, BaseBlogDetailView):


    # model = BlogArticle
    def get_object_query(self, queryset, path):
        return queryset.filter(path=path).select_related('template', 'category').prefetch_related('tags', 'related').get()

    
class BlogTagView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = BlogTag
    pass

class BlogCategoryView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

    # model = BlogCategory
    pass

class BlogListView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, BaseBlogListView):

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



