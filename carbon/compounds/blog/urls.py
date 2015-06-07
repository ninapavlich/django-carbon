from django.conf.urls import patterns, url, include

from .views import *

urlpatterns = patterns('',
	
	# url( (r'^%s$'%settings.BLOG_TAG_DOMAIN), BlogTagListView.as_view(), {'path': "/%s"%(settings.BLOG_TAG_DOMAIN)}, name='blog_tags'),
	# url( (r'^%s$'%settings.BLOG_ARTICLE_DOMAIN), BlogListView.as_view(), {'path': "/%s"%(settings.BLOG_ARTICLE_DOMAIN)}, name='blog_list'),	
	# url( (r'^%s$'%settings.BLOG_CONTRIBUTOR_DOMAIN), BlogContributorListView.as_view(), {'path': "/%s"%(settings.BLOG_CONTRIBUTOR_DOMAIN)}, name='blog_contributors'),	
	# url( (r'^%s(?P<path>[\w-]+)/$'%settings.BLOG_TAG_DOMAIN), BlogTagView.as_view(), name='blog_tag'),
	# url( (r'^%s(?P<path>[\w-]+)/$'%settings.BLOG_CATEGORY_DOMAIN), BlogCategoryView.as_view(), name='blog_category'),
	# url( (r'^%s(?P<path>.*)/$'%settings.BLOG_ARTICLE_DOMAIN), BlogArticleDetailView.as_view(), name='blog_article'),

)