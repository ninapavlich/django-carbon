from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

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
  
    related = models.ManyToManyField('self', blank=True, symmetrical=True)
    tags = models.ManyToManyField('blog.BlogTag', blank=True)
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
    


class BlogComment(UserInputMolecule):
    class Meta:
        abstract = True

    article = models.ForeignKey('blog.BlogArticle')
    in_response_to = models.ForeignKey('self', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)

    @cached_property
    def is_draft(self):
        return self.moderation_status == ModerationAtom.SUBMITTED

    @cached_property
    def is_published(self):
        return self.moderation_status == ModerationAtom.PUBLISHED

    @cached_property
    def is_flagged(self):
        
        max_flags = 1 if not hasattr(settings, 'BLOG_MAX_FLAGS') else settings.BLOG_MAX_FLAGS
        return len(self.get_flags()) >= max_flags

    @cached_property
    def is_rejected(self):
        return self.moderation_status == ModerationAtom.REJECTED

    def downvote(self, user):
        self.vote(user, UpvoteDownvoteFlagMolecule.DOWNVOTE)

    def get_downvotes(self):
        return self.get_votes(UpvoteDownvoteFlagMolecule.DOWNVOTE)

    def upvote(self, user):
        self.vote(user, UpvoteDownvoteFlagMolecule.UPVOTE)

    def get_upvotes(self):
        return self.get_votes(UpvoteDownvoteFlagMolecule.UPVOTE)

    def get_vote_total(self):
        return self.get_upvotes() - self.get_downvotes()


    def vote(self, user, type):
        vote_model = get_model(settings.BLOG_COMMENT_VOTE_MODEL.split('.')[0], settings.BLOG_COMMENT_VOTE_MODEL.split('.')[1])
        vote, vote_created = vote_model.objects.get_or_create(comment=self,voter=user)
        vote.type = type
        vote.save()

    def get_votes(self, type):
        vote_model = get_model(settings.BLOG_COMMENT_VOTE_MODEL.split('.')[0], settings.BLOG_COMMENT_VOTE_MODEL.split('.')[1])
        return vote_model.objects.filter(comment=self)

    def flag(self, user):
        flag_model = get_model(settings.BLOG_COMMENT_FLAG_MODEL.split('.')[0], settings.BLOG_COMMENT_FLAG_MODEL.split('.')[1])
        flag, flag_created = flag_model.objects.get_or_create(comment=self,voter=user)
        flag.type = UpvoteDownvoteFlagMolecule.FLAG
        flag.save()

    def get_flags(self):
        flag_model = get_model(settings.BLOG_COMMENT_FLAG_MODEL.split('.')[0], settings.BLOG_COMMENT_FLAG_MODEL.split('.')[1])
        return flag_model.objects.filter(comment=self)

    

    def generate_title(self):
        words = 12 if not hasattr(settings, 'BLOG_COMMENT_AUTO_TITLE_LENGTH') else settings.BLOG_COMMENT_AUTO_TITLE_LENGTH
        return Truncator(self.content).words(words, html=True)
        

    def save(self, *args, **kwargs):
        allow_html = False if not hasattr(settings, 'BLOG_COMMENT_ALLOW_HTML') else settings.BLOG_COMMENT_ALLOW_HTML
        if not allow_html:
            self.content = strip_tags(self.content)

        max_words = 1000 if not hasattr(settings, 'BLOG_COMMENT_MAX_WORDS') else settings.BLOG_COMMENT_MAX_WORDS
        if max_words:
            self.content = Truncator(self.content).words(max_words, html=True)

        is_new = True if not self.pk else False            

        super(BlogComment, self).save(*args, **kwargs)

        if is_new:
            require_moderation = False if not hasattr(settings, 'BLOG_COMMENT_REQUIRE_MODERATION') else settings.BLOG_COMMENT_REQUIRE_MODERATION
            if require_moderation:
                self.moderation_status = ModerationAtom.SUBMITTED
            else:
                self.moderation_status = ModerationAtom.PUBLISHED
            super(BlogComment, self).save(*args, **kwargs)


    @classmethod
    def get_comments_for_article(cls,article, include_drafts=False, include_rejected=True):
        comments = cls.objects.filter(article=article)

        if include_drafts==False:
            comments = comments.exclude(moderation_status=ModerationAtom.SUBMITTED)

        if include_rejected==False:
            comments = comments.exclude(moderation_status=ModerationAtom.REJECTED)

        return comments

class BlogCommentVote(UpvoteDownvoteFlagMolecule):
    class Meta:
        abstract = True
    
    comment = models.ForeignKey('blog.BlogComment')

class BlogCommentFlag(UpvoteDownvoteFlagMolecule):
    class Meta:
        abstract = True
    
    comment = models.ForeignKey('blog.BlogComment')    


