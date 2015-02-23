from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	
	#/blog/
	#/blog/tags/
	# url( (r'^%s(?P<path>[\w-]+)/$'%settings.BLOG_TAG_DOMAIN), BlogTagView.as_view(), name='blog_tag'),
	# url( (r'^%s(?P<path>[\w-]+)/$'%settings.BLOG_CATEGORY_DOMAIN), BlogCategoryView.as_view(), name='blog_category'),
	# url( (r'^%s(?P<path>[\w-]+)/$'%settings.BLOG_ARTICLE_DOMAIN), BlogArticleDetailView.as_view(), name='blog_article'),
)