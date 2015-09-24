import re
import urllib
from unidecode import unidecode
from django import forms
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import Library, Context, Template
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

from ..models import *


from carbon.compounds.blog.forms import BlogCommentForm

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
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_SUBMIT
    form.fields["article"].initial = article
    form.fields['content'].widget = forms.Textarea()    
    form.fields['content'].initial = ''
    return _render_comment_form(context, form, "Submit")


@register.assignment_tag(takes_context=True)
def get_blog_comment_reply_form(context, comment, form):
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_REPLY
    form.fields['content'].widget = forms.Textarea()    
    form.fields['content'].initial = ''
    # form.fields["reply_to_comment"].initial = comment
    return _render_comment_form(context, form, "Reply")

@register.assignment_tag(takes_context=True)
def get_blog_comment_update_form(context, comment, form):
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_UPDATE
    form.fields['content'].widget = forms.Textarea()    
    form.fields["content"].initial = comment.content    
    
    # form.fields["reply_to_comment"].initial = comment
    # form.fields['content'].widget = forms.TextArea()
    return _render_comment_form(context, form, "Update")

@register.assignment_tag(takes_context=True)
def get_blog_comment_delete_form(context, comment, form):
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_DELETE
    form.fields['content'].widget = forms.HiddenInput()    
    form.fields["content"].initial = ''
    # form.fields["reply_to_comment"].initial = comment
    return _render_comment_form(context, form, "Delete")    

@register.assignment_tag(takes_context=True)
def get_blog_comment_upvote_form(context, comment, form):
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_UPVOTE
    # form.fields["reply_to_comment"].initial = comment
    form.fields['content'].widget = forms.HiddenInput()    
    form.fields["content"].initial = ''
    return _render_comment_form(context, form, "Up Vote")        

@register.assignment_tag(takes_context=True)
def get_blog_comment_downvote_form(context, comment, form):
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_DOWNVOTE
    # form.fields["reply_to_comment"].initial = comment
    form.fields['content'].widget = forms.HiddenInput()    
    form.fields["content"].initial = ''
    return _render_comment_form(context, form, "Down Vote")        

@register.assignment_tag(takes_context=True)
def get_blog_comment_flag_form(context, comment, form):
    form.fields["comment_action"].initial = BlogCommentForm.ACTION_FLAG
    # form.fields["reply_to_comment"].initial = comment
    form.fields['content'].widget = forms.HiddenInput()    
    form.fields["content"].initial = ''
    return _render_comment_form(context, form, "Flag") 

def _render_comment_form(context, form, submit_label):
    
    template_string = '\
    <form action="" method="post" class="{{form_class}}">{% csrf_token %}\
        {{ form.as_p }}\
        <input type="submit" value="{{submit_label}}">\
    </form>'

    template = Template(template_string)
    request = context['request']
    context_dict = {}
    context_dict.update(csrf(request))
    context_dict['form'] = form
    context_dict['submit_label'] = submit_label
    context_dict['form_class'] = slugify(submit_label)
    context = Context(context_dict)
    return template.render(context)