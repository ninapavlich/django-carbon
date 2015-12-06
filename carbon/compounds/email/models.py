import re
import uuid
import datetime
import smtplib
import traceback

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.template import Context
from django.template import Template as DjangoTemplate
from django.utils.translation import ugettext_lazy as _
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model

from carbon.atoms.models.abstract import VersionableAtom
from carbon.atoms.models.access import AccessKeyAtom


from carbon.atoms.models.content import *

class EmailTemplate(VersionableAtom, TitleAtom):

    help = {
        'body_template':"Template used for email body",
        'subject_template':"Template used for email subject",
        'slug':"This slug can be referenced within templates: {% extends template-slug %}"
    }


    body_template = models.TextField(_('body template'), 
        help_text=help['body_template'], null=True, blank=True)
    subject_template = models.TextField(_('subject template'), 
        help_text=help['subject_template'], null=True, blank=True)


    def send_email_message( self, recipient_email, category, message_context={}, html_base_template=None):

        category_settings = get_category_settings_for_user(recipient_email, category)
        if category_settings.can_email() == False:
            #User has opted out
            return

        receipt_model = get_model_by_label(settings.EMAIL_RECEIPT_MODEL)
        receipt = receipt_model.create_receipt(recipient_email, category)


        message_context['email'] = recipient_email
        message_context['receipt'] = receipt
        message_context['category'] = category
        message_context['subscription_settings'] = category_settings.parent
        message_context['category_subscription_settings'] = category_settings
        message_context['settings'] = settings
        message_context['site'] = Site.objects.get_current()
        message_context['site_url'] = 'https://%s'%(Site.objects.get_current()) if settings.USE_SSL else 'http://%s'%(Site.objects.get_current())


        if html_base_template==None:
            model = get_model_by_label(settings.TEMPLATE_MODEL)

            try:
                html_base_template_object = model.objects.get(slug=settings.DEFAULT_EMAIL_TEMPLATE_SLUG)
                html_base_template = DjangoTemplate(html_base_template_object.get_content())
            except:
                raise ImproperlyConfigured( "Default Email template not found. Please check your DEFAULT_EMAIL_TEMPLATE setting.")

        
        # -- Render the Subject of the Email
        subject_template= DjangoTemplate( self.subject_template )
        subject         = subject_template.render( Context( message_context ) )
        subject         = ' '.join(subject.split()) #Remove whitespace, newlines, etc

        # -- Render the Body of the Email
        body_template   = DjangoTemplate( self.body_template )
        body            = body_template.render( Context( message_context ) )
        message         = _totext( body )

        # -- Render the Template
        message_context['subject'] = subject
        message_context['body'] = body
            
        
        message_html = html_base_template.render( Context( message_context ) )

        receipt.rendered(subject, message_html)

        # -- Send Message
        try:
            _send( recipient_email, subject, message, unicode( message_html ) )
        except smtplib.SMTPException:
            print "WARNING: ERROR SENDING EMAIL MESSAGE"
            receipt.record_error( traceback.format_exc() )

    class Meta:
        abstract = True


class EmailCategory(VersionableAtom, TitleAtom, HierarchicalAtom):
    help = {
        'can_be_viewed_online':"Allow recipients to view this online. DO NOT ENABLE if you are sending any kind of private data in this email category.",
        'requires_explicit_opt_in':"Sending these emails require user to explicitely opt-in to category.",
        'can_unsubscribe': "If these emails are transactional, then subscribe/unsubscribe functionality is not needed",
        # 'can_change_frequency': "If these emails be received at a different freququency",
    }

    can_be_viewed_online = models.BooleanField(default=False, help_text=help['can_be_viewed_online'])

    requires_explicit_opt_in = models.BooleanField(default=False, help_text=help['requires_explicit_opt_in'])
    can_unsubscribe = models.BooleanField(default=True, help_text=help['can_unsubscribe'])
    # can_change_frequency = models.BooleanField(default=True, help_text=help['can_change_frequency'])


    def can_view_online(self):
        if self.can_be_viewed_online == False:
            return False

        #Make sure override has not been applied
        if self.parent:
            return self.parent.can_view_online()

        #WE MADE IT!
        return True

    class Meta:
        abstract = True
        verbose_name_plural = 'Email categories'


class EmailReceipt(VersionableAtom, AccessKeyAtom):

    recipient_email = models.CharField(_("Recipient Email"), max_length = 255)
    rendered_subject = models.TextField(_('Rendered Subject'), blank=True, null=True)    
    rendered_body = models.TextField(_('Rendered Body'), blank=True, null=True)

    viewed = models.BooleanField(default=False,)
    viewed_from_email = models.BooleanField(default=False,)
    viewed_online = models.BooleanField(default=False,)
    view_count = models.PositiveIntegerField('View Count', default=0, null = True, blank=True)
    first_viewed_date = models.DateTimeField ( _("First Viewed Date"), blank=True, null=True )
    last_viewed_date = models.DateTimeField ( _("Last Viewed Date"), blank=True, null=True )

    category = models.ForeignKey('email.EmailCategory')

    sending_error = models.BooleanField(default=False,)
    sending_error_message = models.TextField(blank=True, null=True)

    def get_record_url(self):
        try:
            return reverse('email_record_view', kwargs = {'access_key': self.access_key }) 
        except:
            return None

    def get_rendered_url(self):
        try:
            return reverse('email_rendered_view', kwargs = {'access_key': self.access_key })
        except:
            return None

    def get_view_online_url(self):
        if self.category.can_be_viewed_online:
            try:
                return reverse('email_online_view', kwargs = {'access_key': self.access_key })
            except:
                return None
        return None

    def get_absolute_url(self):
        return self.get_view_online_url()

    @property
    def notification_settings(self):
        model = get_model_by_label(settings.EMAIL_NOTIFICATION_CATEGORY_MODEL)
        settings, created = model.objects.get_or_create(category=self.category,recipient_email=self.recipient_email)
        return settings

    def record_view(self, from_email=True, from_online=False):
        if not self.first_viewed_date:
            self.first_viewed_date = datetime.datetime.now()
        
        self.last_viewed_date = datetime.datetime.now()

        self.view_count += 1
        self.viewed = True

        if from_email:
            self.viewed_from_email = True

        if from_online:
            self.viewed_online = True

        self.save()

    def record_error(self, messsage):
        self.sending_error = True
        self.sending_error_message = messsage
        self.save()

    def rendered(self, subject, message):
        self.rendered_subject = subject
        self.rendered_body = message
        self.save()

    def render_counter(self):
        site = Site.objects.get_current() 
        protocol = 'https' if settings.USE_SSL else 'http'
        return '<img src="%s://%s%s" alt="Email Counter" style="width:1px;height:1px;" />'%(protocol, site.domain, self.get_record_url())

    @classmethod
    def create_receipt(cls, recipient_email, category):
        item = cls( recipient_email=recipient_email, category=category )
        item.save()
        return item

    class Meta:
        abstract = True


class UserSubscriptionSettings(VersionableAtom, AccessKeyAtom):
    
    recipient_email = models.CharField(_("Recipient Email"), max_length = 255)

    def get_absolute_url(self):
        try:
            return reverse('email_settings_view', kwargs = {'access_key': self.access_key })
        except:
            return None

    def get_settings(self, category=None):
        model = get_model_by_label(settings.EMAIL_CATEGORY_SUBSCRIPTION_MODEL)

        if category:
            category_settings, created = model.objects.get_or_create(parent=self,category=category)
            return category_settings
            
        else:
            return model.objects.filter(parent=self)

    
    def __unicode__(self):
        return "Subscription settings for %s"%(self.recipient_email)

    class Meta:
        abstract = True
        verbose_name_plural = 'User subscription settings'

class EmailCategorySubscriptionSettings(VersionableAtom, TitleAtom):

    parent = models.ForeignKey('email.UserSubscriptionSettings')

    category = models.ForeignKey('email.EmailCategory')

    DEFAULT = 'default'
    UNSUBSCRIBED = 'unsubscribed'
    SUBSCRIBED = 'subscribed'
    NOTIFICATION_STATUS_CHOICES = (
        (DEFAULT, _("Default")),
        (UNSUBSCRIBED, _("Unsubscribed")),
        (SUBSCRIBED, _("Subscribed")),
    )

    status = models.CharField(choices=NOTIFICATION_STATUS_CHOICES, 
        default=DEFAULT, max_length = 255)


    
    def can_email(self):
        if self.category.requires_explicit_opt_in:
            if self.status != EmailCategorySubscriptionSettings.SUBSCRIBED:
                return False
        elif self.category.can_unsubscribe:
            if self.status == EmailCategorySubscriptionSettings.UNSUBSCRIBED:
                return False

        
        #WE MADE IT!
        return True

    def save(self, *args, **kwargs):

        self.title = "Subscription settings for %s - %s"%(self.parent.recipient_email, self.category.title)           
        super(EmailCategorySubscriptionSettings, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True
        verbose_name_plural = 'Email Category subscription settings'



def get_settings_for_user(recipient_email, category=None):
    notification_settings_model = get_model_by_label(settings.EMAIL_SUBSCRIPTION_MODEL)
    notification_settings, created = notification_settings_model.objects.get_or_create(recipient_email=recipient_email)

    return notification_settings

def get_category_settings_for_user(recipient_email, category=None):
    notification_settings_model = get_model_by_label(settings.EMAIL_SUBSCRIPTION_MODEL)
    notification_settings, created = notification_settings_model.objects.get_or_create(recipient_email=recipient_email)

    if category:
        return notification_settings.get_settings(category)
    else:
        return notification_settings.get_settings()       


def get_model_by_label(label):
    app_label = label.split('.')[0]
    object_name = label.split('.')[1]
    return get_model(app_label, object_name)

def _totext( data ):
    """Strips HTML from Email for Text Only"""
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def _get_formatted_sender():
    try:
        return "%s <%s>" % ( settings.DEFAULT_FROM_EMAIL_NAME, settings.DEFAULT_FROM_EMAIL)
    except:
        raise ImproperlyConfigured( "The following variables must be defined in settings in order to use the emailer: DEFAULT_FROM_EMAIL_NAME, DEFAULT_FROM_EMAIL" )

def _get_formatted_recipient( recipient_email ):
    """Ensure Email Address is Returned in a List"""
    if isinstance( recipient_email, str ):
        return [ recipient_email ]
    elif isinstance( recipient_email, unicode ):
        return [ recipient_email ]
    else:
        return recipient_email

def _send( recipient_email, subject, message, message_html = None ):
    
    # -- Create Message
    msg = EmailMultiAlternatives( subject, message, _get_formatted_sender(), _get_formatted_recipient( recipient_email ) )

    # -- Attach HTML Message
    if message_html:
        msg.attach_alternative( message_html, "text/html; charset=UTF-8" )

    # -- Send Message
    msg.send()



