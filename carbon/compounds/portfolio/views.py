from django.views.generic import DetailView
from carbon.atoms.views.abstract import *
from carbon.atoms.views.content import *

from .models import *


class ProjectDetailView(NonAdminCachableView, PublishableView, AddressibleView, DetailView):

    # model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        
        categories = self.object.get_categories()
        context['categories'] = categories
        
        category_request = self.request.GET.get('category', None)
        print 'category_request? %s'%(category_request)
        if category_request:
        	for category in categories:
        		if category.slug == category_request:
        			context['category'] = category
        			context['previous_by_category'] = category.get_next_item(self.object)
        			context['next_by_category'] = category.get_previous_item(self.object)

        print context

        return context



class ProjectCategoryView(NonAdminCachableView, PublishableView, AddressibleView, HasChildrenView, DetailView):

    # model = ProjectCategory
    pass