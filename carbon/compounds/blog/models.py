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


class BlogRelatedObject(LinkAtom):
    symmetrical=True
    
    #Point to an object
    article = models.ForeignKey('blog.BlogArticle')

    try:
        content_type = models.ForeignKey(ContentType, 
            limit_choices_to={"model__in": settings.BLOG_RELATED_MODEL_CHOICES}, 
            null=True, blank=True)
    except:
        content_type = models.ForeignKey(ContentType, null=True, blank=True)

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')    

    def get_absolute_url(self):
        if self.content_object:
            if hasattr(self.content_object, 'get_absolute_url'):
                return self.content_object.get_absolute_url()        
        return self.path_override

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if not self.title and self.content_object:
            if hasattr(self.content_object, 'title'):
                self.title = self.content_object.title

        if self.symmetrical and self.content_object:
            this_ct = ContentType.objects.get_for_model(self.article)
            related_ct = ContentType.objects.get_for_model(self.content_object)
            
            if this_ct == related_ct:
                opposite, created = self.__class__.objects.get_or_create(
                    article=self.content_object, object_id=self.article.id, 
                    content_type=this_ct)

        super(BlogRelatedObject, self).save(*args, **kwargs)


class BlogArticle(ContentMolecule):
    # default_template = 'blog_article'

    help = {
        'allow_comments': "Allow comments on article"
    }

    class Meta:
        abstract = True
   
    allow_comments = models.BooleanField(default=False, 
        help_text=help['allow_comments'])
  
    tags = models.ManyToManyField('blog.BlogTag', blank=True, null=True)
    category = models.ForeignKey('blog.BlogCategory', blank=True, null=True, 
        on_delete=models.SET_NULL)

    # def get_related(self):
    #     return BlogRelatedObject.objects.filter(article=self).order_by('order')

    def build_path(self):

        if self.category:
            return "%s%s/" % (self.category.path, self.slug)
        else:
            return "/%s%s/" % (settings.BLOG_ARTICLE_DOMAIN, self.slug)

    def get_absolute_url(self):
        return reverse_lazy('blog_article', kwargs = {'path': self.get_url_path() }) 