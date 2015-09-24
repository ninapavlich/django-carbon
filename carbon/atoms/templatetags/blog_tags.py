import re
import urllib
from unidecode import unidecode
from django import forms
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import Library


try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

from ..models import *


# from carbon.compounds.blog.forms import BlogCommentForm

register = Library()


@register.assignment_tag(takes_context=True)
def can_user_edit_comment(context, comment):
    request = context['request']
    return request.user == comment.user

@register.assignment_tag()
def get_blog_article_comments(article):
    blog_comment_model = get_model(settings.BLOG_COMMENT_MODEL.split('.')[0], settings.BLOG_COMMENT_MODEL.split('.')[1])
    return blog_comment_model.get_comments_for_article(article)


@register.assignment_tag(takes_context=True)
def get_blog_comment_form(context, article, form):
    
    form_class = type(form)
    return form_class.create_submit_form(context, form, article)


@register.assignment_tag(takes_context=True)
def get_blog_comment_reply_form(context, comment, form):

    form_class = type(form)
    return form_class.create_reply_form(context, form, comment)
    

@register.assignment_tag(takes_context=True)
def get_blog_comment_update_form(context, comment, form):

    form_class = type(form)
    return form_class.create_update_form(context, form, comment)

@register.assignment_tag(takes_context=True)
def get_blog_comment_delete_form(context, comment, form):

    form_class = type(form)
    return form_class.create_delete_form(context, form, comment)

@register.assignment_tag(takes_context=True)
def get_blog_comment_upvote_form(context, comment, form):
    form_class = type(form)
    return form_class.create_upvote_form(context, form, comment)      

@register.assignment_tag(takes_context=True)
def get_blog_comment_downvote_form(context, comment, form):
    form_class = type(form)
    return form_class.create_downvote_form(context, form, comment)            

@register.assignment_tag(takes_context=True)
def get_blog_comment_flag_form(context, comment, form):
    form_class = type(form)
    return form_class.create_flag_form(context, form, comment)            
