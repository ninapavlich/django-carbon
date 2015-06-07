from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.abstract import VersionableAtom

from carbon.atoms.models.content import *

class BlogTag(TagMolecule):
    publish_by_default = True
    # default_template = 'blog_tag'
    # item_class = BlogArticle
    # url_domain = settings.BLOG_TAG_DOMAIN

    class Meta:
        abstract = True

    def get_absolute_url(self):
        if self.is_external:
            return self.path_override
        return reverse_lazy('blog_tag', kwargs = {'path': self.get_url_path() })   

class BlogCategory(CategoryMolecule):
    publish_by_default = True
    # default_template = 'blog_category'
    # item_class = BlogArticle
    # url_domain = settings.BLOG_CATEGORY_DOMAIN

    class Meta:
        verbose_name_plural = 'Blog categories'
        abstract = True

    def get_absolute_url(self):
        if self.is_external:
            return self.path_override
        return reverse_lazy('blog_category', kwargs = {'path': self.get_url_path() })   

class BlogArticleRole(VersionableAtom):
    # url_domain = settings.BLOG_ARTICLE_DOMAIN

    class Meta:
        abstract = True

    help = {
        'order': "Display order",
        'role': "Role that user plays in this article"
    }

    try:
        BLOG_ROLE_CHOICES = settings.BLOG_ROLE_CHOICES        
    except:
        AUTHOR = 'author'
        EDITOR = 'editor'
        PUBLISHER = 'publisher'
        BLOG_ROLE_CHOICES = (
            (AUTHOR, _("Author")),
            (EDITOR, _("Editor")),
            (PUBLISHER, _("Publisher")),
        )

    order = models.IntegerField(default=0, help_text=help['order'])   
    
    # YOU GOTTA IMPLEMENT THIS:
    article = models.ForeignKey('blog.BlogArticle')
    user = models.ForeignKey(settings.BLOG_ROLE_USER_MODEL)
    role = models.CharField(_('Role'), max_length=255, 
        choices=BLOG_ROLE_CHOICES, help_text=help['role'])


class BlogArticle(ContentMolecule):
    # default_template = 'blog_article'

    help = {
        'allow_comments': "Allow comments on article"
    }

    class Meta:
        abstract = True
   
    allow_comments = models.BooleanField(default=False, 
        help_text=help['allow_comments'])
  
    related = models.ManyToManyField('self', blank=True, null=True, symmetrical=True)
    tags = models.ManyToManyField('blog.BlogTag', blank=True, null=True)
    category = models.ForeignKey('blog.BlogCategory', blank=True, null=True, 
        on_delete=models.SET_NULL)

    def build_path(self):

        if self.category:
            return "%s%s/" % (self.category.path, self.slug)
        else:
            return "/%s/" % self.slug

    def get_absolute_url(self):
        if self.is_external:
            return self.path_override
        return reverse_lazy('blog_article', kwargs = {'path': self.get_url_path() }) 


