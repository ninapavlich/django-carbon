from django import forms
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

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
    content = forms.CharField(required=False, widget=forms.Textarea())
    reply_to_comment = forms.ModelChoiceField(queryset=blog_comment_model.objects.all(), required=False)
        # , widget=forms.HiddenInput())
    article = forms.ModelChoiceField(queryset=blog_article_model.objects.all(), required=False, widget=forms.HiddenInput())
    
    def __init__( self, request, *args, **kwargs ):
        super( BlogCommentForm, self ).__init__( *args, **kwargs )
        self.request = request

    def clean_comment_action(self):
        
        #Require logged in user
        if not self.request.user or not self.request.user.is_authenticated():
            raise forms.ValidationError(_("Please log in to comment"))

        return self.data['comment_action']


    def clean_content(self):
        
        comment_action = self.data['comment_action']
        comment_content = self.cleaned_data['content']
        
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


    def clean_reply_to_comment(self):
        
        comment_action = self.data['comment_action']
        comment_reply_to_comment = self.cleaned_data['reply_to_comment']
        
        if comment_action == BlogCommentForm.ACTION_REPLY:
            if not comment_reply_to_comment:
                raise forms.ValidationError(_("Please enter a comment to reply to"))

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
        print "TODO: Reply to comment"

    def update_comment(self):
        print "TODO: edit comment"

    def delete_comment(self):
        print "TODO: delete"


    def upvote_comment(self):
        print "TODO: upvote"

    def downvote_comment(self):
        print "TODO: downvote"

    def flag_comment(self):
        print "TODO: flag"

    
    
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


