from django.utils import timezone

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

    def build_path(self, path_attribute='slug', parent_path_attribute='path'):

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
        ordering = ['created_date']
   

    article = models.ForeignKey('blog.BlogArticle')


    in_response_to = models.ForeignKey('self', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)

    @cached_property
    def level(self):
        if not self.in_response_to:
            return 1
        else:
            return self.in_response_to.level+1

    @cached_property
    def is_draft(self):
        return self.moderation_status == ModerationAtom.SUBMITTED

    @cached_property
    def is_published(self):
        return (self.moderation_status == ModerationAtom.PUBLISHED or self.moderation_status == ModerationAtom.APPROVED)

    @cached_property
    def is_visible(self):
        return self.is_published and self.is_flagged==False and self.is_rejected==False and self.is_deleted==False

    @cached_property
    def is_flagged(self):
        #if this has been manually approved, then its not flagged
        if self.moderation_status == ModerationAtom.APPROVED:
            return False
        max_flags = 1 if not hasattr(settings, 'BLOG_MAX_FLAGS') else settings.BLOG_MAX_FLAGS
        return len(self.get_flags()) >= max_flags

    @cached_property
    def is_rejected(self):
        return self.moderation_status == ModerationAtom.REJECTED

    def downvote(self, user):
        self.vote(user, UpvoteDownvoteFlagMolecule.DOWNVOTE)

    @cached_property
    def downvotes(self):
        return self.get_votes(UpvoteDownvoteFlagMolecule.DOWNVOTE)

    def get_downvotes_total(self):
        return len(self.downvotes)

    def upvote(self, user):
        self.vote(user, UpvoteDownvoteFlagMolecule.UPVOTE)

    @cached_property
    def upvotes(self):
        return self.get_votes(UpvoteDownvoteFlagMolecule.UPVOTE)

    def get_upvotes_total(self):
        return len(self.upvotes)

    def get_vote_total(self):
        return self.get_upvotes_total() - self.get_downvotes_total()


    def vote(self, user, type):
        vote_model = get_model(settings.BLOG_COMMENT_VOTE_MODEL.split('.')[0], settings.BLOG_COMMENT_VOTE_MODEL.split('.')[1])
        vote, vote_created = vote_model.objects.get_or_create(comment=self,voter=user)
        vote.type = type
        vote.save()

    def get_votes(self, type):
        vote_model = get_model(settings.BLOG_COMMENT_VOTE_MODEL.split('.')[0], settings.BLOG_COMMENT_VOTE_MODEL.split('.')[1])
        return vote_model.objects.filter(comment=self,type=type)

    def flag(self, user):
        flag_model = get_model(settings.BLOG_COMMENT_FLAG_MODEL.split('.')[0], settings.BLOG_COMMENT_FLAG_MODEL.split('.')[1])
        flag, flag_created = flag_model.objects.get_or_create(comment=self,voter=user)
        flag.type = UpvoteDownvoteFlagMolecule.FLAG
        flag.save()

    def get_flags(self):
        flag_model = get_model(settings.BLOG_COMMENT_FLAG_MODEL.split('.')[0], settings.BLOG_COMMENT_FLAG_MODEL.split('.')[1])
        return flag_model.objects.filter(comment=self)

    @property
    def can_update(self):

        max_age_minutes = 60 if not hasattr(settings, 'BLOG_COMMENT_ALLOW_EDIT_MAX_AGE_MINUTES') else settings.BLOG_COMMENT_ALLOW_EDIT_MAX_AGE_MINUTES
        if max_age_minutes == 0:
            return False

        #TODO: wonder if i should use modified_date or created_date here...
        comment_age = timezone.now() - self.created_date
        comment_age_minutes = (comment_age.days * (24*60)) + (comment_age.seconds/60)

        return comment_age_minutes <= max_age_minutes

    def attempt_to_update(self, new_content):
        
        if self.can_update:
            self.content = new_content
            self.save()
            return True

        return False

    @property
    def can_reply(self):
        max_reply_levels = 2 if not hasattr(settings, 'BLOG_COMMENT_MAX_REPLY_LEVELS') else settings.BLOG_COMMENT_MAX_REPLY_LEVELS
        return self.level < max_reply_levels

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
    def _build_comment_tree(cls, parent, level=0, list=None, branch=None):
        if not list:
            list = []

        if branch:
            list.append(branch)
        comment_children = cls.objects.filter(parent=parent,in_response_to=branch)
        for child in comment_children:
            list = cls._build_comment_tree(parent, level+1, list, child)
        return list



    @classmethod
    def get_comments_for_parent(cls,parent, include_drafts=False, include_rejected=True):
        tree = cls._build_comment_tree(parent)

        if include_drafts==False:
            tree = [item for item in tree if item.moderation_status!=ModerationAtom.SUBMITTED]
            # comments = comments.exclude(moderation_status=ModerationAtom.SUBMITTED)

        if include_rejected==False:
            tree = [item for item in tree if item.moderation_status!=ModerationAtom.REJECTED]
            # comments = comments.exclude(moderation_status=ModerationAtom.REJECTED)


        return tree

class BlogCommentVote(UpvoteDownvoteFlagMolecule):
    class Meta:
        abstract = True
    
    comment = models.ForeignKey('blog.BlogComment')

class BlogCommentFlag(UpvoteDownvoteFlagMolecule):
    class Meta:
        abstract = True
    
    comment = models.ForeignKey('blog.BlogComment')    


