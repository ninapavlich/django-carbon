import re
import uuid

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.template import Context
from django.template import Template
from django.utils.translation import ugettext_lazy as _


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


    def send_email_message( self, recipient_email, category, context={}, html_base_template=None):

        if html_base_template==None:
            app_label = settings.TEMPLATE_MODEL.split('.')[0]
            object_name = settings.TEMPLATE_MODEL.split('.')[1]
            model = get_model(app_label, object_name)

            try:
                html_base_template_object = model.objects.get(slug=settings.DEFAULT_EMAIL_TEMPLATE_SLUG)
                html_base_template = Template(html_base_template_object.get_content())
            except:
                raise ImproperlyConfigured( "Default Email template not found. Please check your DEFAULT_EMAIL_TEMPLATE setting.")

        
        # -- Render the Subject of the Email
        subject_template= Template( self.subject_template )
        subject         = subject_template.render( Context( context ) )

        # -- Render the Body of the Email
        body_template   = Template( self.body_template )
        body            = body_template.render( Context( context ) )
        message         = _totext( body )

        # -- Render the Template

        app_label = settings.EMAIL_RECEIPT_MODEL.split('.')[0]
        object_name = settings.EMAIL_RECEIPT_MODEL.split('.')[1]
        receipt_model = get_model(app_label, object_name)

        receipt = receipt_model.create_receipt(recipient_email, category)
        message_context = { 
            'subject' : subject, 
            'email' : recipient_email, 
            'body' : body, 
            'receipt': receipt, 
            'category':category,
            'settings':settings,
            'site':Site.objects.get_current()
        }
        message_html = html_base_template.render( Context( message_context ) )

        receipt.rendered(subject, message_html)

        # -- Send Message
        _send( recipient_email, subject, message, unicode( message_html ) )

    class Meta:
        abstract = True


class EmailCategory(VersionableAtom, TitleAtom, HierarchicalAtom):
    help = {
        'can_be_viewed_online':"Allow recipients to view this online. DO NOT ENABLE if you are sending any kind of private data in this email category.",
        'requires_explicit_opt_in':"Sending these emails require user to explicitely opt-in to category."
    }

    can_be_viewed_online = models.BooleanField(default=False, help_text=help['can_be_viewed_online'])

    requires_explicit_opt_in = models.BooleanField(default=False, help_text=help['requires_explicit_opt_in'])


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


class EmailReceipt(VersionableAtom):

    recipient_email = models.CharField(_("Recipient Email"), max_length = 255)
    rendered_subject = models.TextField(_('Rendered Subject'), blank=True, null=True)    
    rendered_body = models.TextField(_('Rendered Body'), blank=True, null=True)

    access_key = models.CharField(_("key"), max_length=50, blank=True, null=True, unique=True)
    viewed = models.BooleanField(default=False,)
    view_count = models.PositiveIntegerField('View Count', default=0, null = True, blank=True)
    first_viewed_date = models.DateTimeField ( _("First Viewed Date"), blank=True, null=True )
    last_viewed_date = models.DateTimeField ( _("Last Viewed Date"), blank=True, null=True )

    category = models.ForeignKey('email.EmailCategory')

    def save(self):
        if not self.access_key:
            self.access_key = uuid.uuid1().hex            
        super(EmailReceipt, self).save()     


    def get_record_url(self):
        try:
            return reverse('email_record_view', kwargs = {'access_key': self.access_key }) 
        except:
            return None

    def get_record_url(self):
        try:
            return reverse('email_online_view', kwargs = {'access_key': self.access_key }) 
        except:
            return None

    def get_view_online_url(self):
        if self.category.can_be_viewed_online:
            try:
                return reverse('email_online_view', kwargs = {'access_key': self.access_key })
            except:
                return None
        return None

    @property
    def notification_settings(self):
        settings, created = EmailNotificationCategory.objects.get_or_create(category=self.category,recipient_email=self.recipient_email)
        return settings

    def record_view(self):
        if not self.first_viewed_date:
            self.first_viewed_date = datetime.now()
        
        self.last_viewed_date = datetime.now()

        self.view_count += 1
        self.viewed = True

        self.save()

    def rendered(self, subject, message):
        self.rendered_subject = subject
        self.rendered_body = message
        self.save()

    def render_counter(self):
        site = Site.objects.get_current() 
        protocol = 'https' if settings.USE_SSL else 'http'
        return '<img src="%s://%s%s" alt="Email Counter" style="width:1px;height:1px;" />'%(protocol, site.domain, self.get_absolute_url())

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
            return reverse('email_user_subscription_settings', kwargs = {'access_key': self.access_key })
        except:
            return None

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
            if self.status != EmailNotificationSettings.SUBSCRIBED:
                return False
        else:
            if self.status == EmailNotificationSettings.UNSUBSCRIBED:
                return False

        #Make sure override unsubscribe has not been applied
        if self.category.parent:
            settings, created = cls.objects.get_or_create(category=self.category.parent,recipient_email=self.recipient_email)
            return settings.can_email()

        #WE MADE IT!
        return True

    class Meta:
        abstract = True
        verbose_name_plural = 'Email Category subscription settings'



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



