from django import forms
from django.conf import settings
from django.contrib import messages
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.context_processors import csrf

from ckeditorfiles.widgets import CKEditorWidget

from .models import *

blog_article_model = get_model(settings.BLOG_ARTICLE_MODEL.split('.')[0], settings.BLOG_ARTICLE_MODEL.split('.')[1])
blog_comment_model = get_model(settings.BLOG_COMMENT_MODEL.split('.')[0], settings.BLOG_COMMENT_MODEL.split('.')[1])

class BlogCommentForm(forms.Form):

    ACTION_SUBMIT = 'submit'
    ACTION_REPLY = 'reply'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_UPVOTE = 'upvote'
    ACTION_DOWNVOTE = 'downvote'
    ACTION_FLAG = 'flag'

    BLOG_COMMENT_ACTION_CHOICES = (
        (ACTION_SUBMIT, _("Submit")),
        (ACTION_REPLY, _("Reply")),
        (ACTION_UPDATE, _("Update")),
        (ACTION_DELETE, _("Delete")),
        (ACTION_UPVOTE, _("Upvote")),
        (ACTION_DOWNVOTE, _("Downvote")),
        (ACTION_FLAG, _("Flag")),
    )


    

    comment_action = forms.ChoiceField(required=True,choices=BLOG_COMMENT_ACTION_CHOICES, widget=forms.HiddenInput())
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': _("Comment")}), label=_("Comment"))
    article = forms.ModelChoiceField(queryset=blog_article_model.objects.all(), required=False, widget=forms.HiddenInput())
    reply = forms.ModelChoiceField(queryset=blog_comment_model.objects.all(), required=False, widget=forms.HiddenInput())
    
    def __init__( self, request, was_posted, *args, **kwargs ):
        super( BlogCommentForm, self ).__init__( *args, **kwargs )
        self.request = request
        self.was_posted = was_posted

    def clean_comment_action(self):
        
        #Require logged in user
        if not self.request.user or not self.request.user.is_authenticated():
            raise forms.ValidationError(_("Please log in to comment"))

        return self.data['comment_action']


    def clean_content(self):
        
        comment_action = self.data['comment_action']
        comment_content = self.cleaned_data['content']
        
        if not self.was_posted:
            return comment_content
        # raise forms.ValidationError(_("This is a validation test"))

        if comment_action == BlogCommentForm.ACTION_SUBMIT:
            if not comment_content:
                raise forms.ValidationError(_("Please enter a comment"))

        elif comment_action == BlogCommentForm.ACTION_REPLY:
            if not self.cleaned_data['content']:
                raise forms.ValidationError(_("Please enter a comment"))

        elif comment_action == BlogCommentForm.ACTION_UPDATE:
            if not self.cleaned_data['content']:
                raise forms.ValidationError(_("Please enter a comment"))

        return comment_content


    def clean_reply(self):
        
        comment_action = self.data['comment_action']
        comment_reply_to_comment = self.cleaned_data['reply']
        
        if not self.was_posted:
            return comment_reply_to_comment

        if comment_action == BlogCommentForm.ACTION_REPLY:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to reply to"))

            if not comment_reply_to_comment.can_reply:
                raise forms.ValidationError(_("You cannot reply to this comment"))  

        elif comment_action == BlogCommentForm.ACTION_UPDATE:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to update"))

        elif comment_action == BlogCommentForm.ACTION_FLAG:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to flag"))

        elif comment_action == BlogCommentForm.ACTION_UPVOTE:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to upvote"))

        elif comment_action == BlogCommentForm.ACTION_DOWNVOTE:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to downvote"))

        elif comment_action == BlogCommentForm.ACTION_DELETE:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to delete"))

        return comment_reply_to_comment



    def clean_article(self):
     
        comment_action = self.data['comment_action']
        comment_article = self.cleaned_data['article']

        if not self.was_posted:
            return comment_article
        
        if comment_action == BlogCommentForm.ACTION_SUBMIT:
            if not comment_article:
                raise forms.ValidationError(_("Please enter an article to comment on"))

        return comment_article

    def save(self):
        comment_action = self.data['comment_action']
        
        if comment_action == BlogCommentForm.ACTION_SUBMIT:
            return self.submit_comment()

        elif comment_action == BlogCommentForm.ACTION_REPLY:
            return self.reply_to_comment()

        elif comment_action == BlogCommentForm.ACTION_UPDATE:
            return self.update_comment()
        
        elif comment_action == BlogCommentForm.ACTION_DELETE:
            return self.delete_comment()


        elif comment_action == BlogCommentForm.ACTION_FLAG:
            return self.flag_comment()

        elif comment_action == BlogCommentForm.ACTION_UPVOTE:
            return self.upvote_comment()

        elif comment_action == BlogCommentForm.ACTION_DOWNVOTE:
            return self.downvote_comment()

        
        return data


    def submit_comment(self):
        
        comment = blog_comment_model(
            user = self.request.user,
            content=self.cleaned_data['content'],
            article=self.cleaned_data['article']
        )
        comment.save()

        messages.success(self.request, _("Your comment has been submitted"))

        return comment

    def reply_to_comment(self):
        
        comment = blog_comment_model(
            user = self.request.user,
            content=self.cleaned_data['content'],
            article=self.cleaned_data['article'],
            in_response_to=self.cleaned_data['reply']
        )
        comment.save()

        messages.success(self.request, _("Your reply has been submitted"))

        return comment

    def update_comment(self):
        current_comment = self.cleaned_data['reply']
        updated = current_comment.attempt_to_update(self.cleaned_data['content'])
        if updated:
            messages.success(self.request, _("Your comment has been updated"))
        else:
            messages.success(self.request, _("Your comment can no longer be updated"))

        return current_comment

    def delete_comment(self):
        reply = self.cleaned_data['reply']
        reply.is_deleted = True
        reply.save()
        messages.success(self.request, _("Your comment has been deleted"))
        return reply


    def upvote_comment(self):
        comment = self.cleaned_data['reply']
        comment.upvote(self.request.user)

        messages.success(self.request, _("Thanks for the feedback! This comment has been up-voted."))

    def downvote_comment(self):
        comment = self.cleaned_data['reply']
        comment.downvote(self.request.user)

        messages.success(self.request, _("Thanks for the feedback! This comment has been down-voted."))

    def flag_comment(self):
        comment = self.cleaned_data['reply']
        comment.flag(self.request.user)

        messages.success(self.request, _("Thanks for the feedback! This comment has been flagged to be moderated."))

    @classmethod
    def create_submit_form(cls, context, form_template, article):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_SUBMIT, article, None )      

    @classmethod
    def create_reply_form(cls, context, form_template, comment):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_REPLY, comment.article, comment)

    @classmethod
    def create_update_form(cls, context, form_template, comment):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_UPDATE, comment.article, comment)

    @classmethod
    def create_delete_form(cls, context, form_template, comment):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_DELETE, comment.article, comment)

    @classmethod
    def create_flag_form(cls, context, form_template, comment):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_FLAG, comment.article, comment)

    @classmethod
    def create_upvote_form(cls, context, form_template, comment):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_UPVOTE, comment.article, comment)

    @classmethod
    def create_downvote_form(cls, context, form_template, comment):
        return cls._create_comment_form(context, form_template, BlogCommentForm.ACTION_DOWNVOTE, comment.article, comment)

    @classmethod
    def _create_comment_form(cls, context, form_template, method, article, comment=None):
        request = context['request']

        content_ediable_actions = [
            BlogCommentForm.ACTION_SUBMIT,
            BlogCommentForm.ACTION_UPDATE,
            BlogCommentForm.ACTION_REPLY
        ]
        if method in content_ediable_actions:
            widgets = {'content':forms.Textarea(attrs={'placeholder': _("Comment")})}    
        else:
            widgets = {'content':forms.HiddenInput()}

        initial_values = {}
        initial_values['comment_action'] = method
        initial_values['article'] = article
        
        if method == BlogCommentForm.ACTION_UPDATE:
            initial_values['content'] = comment.content
        else:
            initial_values['content'] = ""

        if comment:
            initial_values['reply'] = comment

        data = None
        was_posted = False

        if request.POST:
            was_posted = request.POST['comment_action'] == method
            is_related_form = True if not comment else str(comment.pk) == str(request.POST['reply'])
            data = {}
            data['article'] = article.pk
            if comment:
                data['reply'] = comment.pk
            data['comment_action'] = method
            data['content'] = request.POST['content'] if (was_posted and is_related_form) else ""        
            
        button_label = dict(BlogCommentForm.BLOG_COMMENT_ACTION_CHOICES).get(method)
        form_id = "comment-%s-form"%(method) if not comment else "comment-%s-%s-form"%(method, comment.pk)
        return cls.create_and_render_form(request, (was_posted and is_related_form), form_template, initial_values, widgets, button_label, form_id, data)

    
    @classmethod
    def create_and_render_form(cls, request, was_posted, form_template, initial_values, widgets, submit_label, form_id, data=None, files=None):

        form = cls.create_form(request, was_posted, form_template, initial_values, widgets, data, files)
        return cls.render_form(form, request, submit_label, form_id)

    @classmethod
    def create_form(cls, request, was_posted, form_template, initial_values, widgets, data=None, files=None):
        kwargs = {
            'initial': initial_values,
            'prefix': None,
        }
        kwargs['request'] = request
        kwargs['was_posted'] = was_posted

        if data:
            kwargs['data'] = data

        if files:
            kwargs['files'] = files
        

        new_form = cls(**kwargs)
        
        for widget_key, widget in widgets.iteritems():
            new_form.fields[widget_key].widget = widget

        #Now set initial values:
        if data:
            for data_key, data in data.iteritems():
                new_form.fields[data_key].initial = data




        return new_form

    @classmethod
    def render_form(cls, form, request, submit_label, form_id):
            
        template_string = '\
        <form action="" method="post" class="{{form_class}}" id="{{form_id}}">{% csrf_token %}\
            {{ form.as_ul }}\
            <input type="submit" value="{{submit_label}}">\
        </form>'

        template = Template(template_string)
        context_dict = {}
        context_dict.update(csrf(request))
        context_dict['form'] = form
        context_dict['submit_label'] = submit_label
        error_class = '' if not form.was_posted else 'valid' if bool(form._errors) else 'invalid'
        context_dict['form_class'] = "%s %s"%(error_class, slugify(submit_label))
        context_dict['form_id'] = form_id
        context = Context(context_dict)
        return template.render(context)
    

#=============================================
# Admin Forms ================================
#=============================================

class BlogArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogarticle_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogarticle_synopsis_ckeditor']), required=False)
    class Meta:
        model = BlogArticle
        fields = '__all__'

class BlogCategoryAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogcategory_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogcategory_synopsis_ckeditor']), required=False)
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogTagAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogtag_content_ckeditor']), required=False)
    synopsis = forms.CharField(widget=CKEditorWidget(config=settings.CKEDITOR_CONFIGS['blogtag_synopsis_ckeditor']), required=False)
    class Meta:
        model = BlogTag
        fields = '__all__'


