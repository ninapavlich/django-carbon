from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import *

class AccessAtom(models.Model):

    help = {
        'access':"Access level",
    }

    OWNER = 10
    WRITE = 20
    READ = 30
    ACCESS_CHOICES = (
        (OWNER, _("Owner")),
        (WRITE, _("Can Edit")),
        (READ, _("Can View")),
    )

    access = models.IntegerField(choices=ACCESS_CHOICES, 
        help_text=help['access'])


# -- Level 4
class AccessibleAtom(models.Model):

    help = {
        'password':"Password to use if access_restriction is set to Password",
        'publish_on_date': "Object state will be set to 'Published' on this date.",
        'expire_on_date': "Object state will be set to 'Expired' on this date.",
        'require_registered_user' : "Require logged in user" 
    }

    # OPEN = 1
    # REGISTERED_USERS = 2
    # PASSWORD = 3
    # USER_WHITELIST = 4
    # USER_BLACKLIST = 5
    # CUSTOM = 6
    # ACCESS_CHOICES = (
    #     (OPEN, _("Open")),
    #     (REGISTERED_USERS, _("Registered Users")),
    #     (PASSWORD, _("Password")),
    #     (USER_WHITELIST, _("User Whitelist")),
    #     (USER_BLACKLIST, _("User Blacklist")),
    #     (CUSTOM, _("Custom")),
    # )


    require_registered_user = models.BooleanField( _("Required Registered Users"), 
        default = False, help_text=help['require_registered_user'])

    password = models.CharField(_('Encrypted Password'), max_length=255, 
        null=True, blank=True, help_text=help['password'])

    #THOUGHT: Not sure if I love this design
    user_whitelist = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_whitelist_user')

    user_blacklist = models.ManyToManyField(settings.AUTH_USER_MODEL, 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_blacklist_user')

    groups_whitelist = models.ManyToManyField('auth.Group', 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_whitelist_groups')

    groups_blacklist = models.ManyToManyField('auth.Group', 
        blank=True, null=True, related_name='%(app_label)s_%(class)s_blacklist_groups')

    publish_on_date = models.DateTimeField(_('Publish on Date'), auto_now=True, 
        blank=True, null=True, help_text=help['publish_on_date'])
    expire_on_date = models.DateTimeField(_('Expire on Date'), auto_now=True, 
        blank=True, null=True, help_text=help['expire_on_date'])

    class Meta:
        abstract = True

    def access_allowed(self, request):
        
        if self.require_registered_user: 
            if not request.user or not request.user.is_authenticated():
                return False


        # elif self.access_restriction == PASSWORD:
        #     #Check if there is a password stored in the cookies
        #     #If not, prompt for password
        #     pass

        user_whitelist = self.user_whitelist.all()
        if len(user_whitelist) > 0:
            if not request.user or not request.user.is_authenticated() \
            or not request.user in user_whitelist:
                return False

        elif self.access_restriction == PASSWORD.CUSTOM:
            custom = self.custom_access_allowed(request)
            if custom == False:
                return False
        
        if self.publish_on_date and now() < self.publish_on_date:
            return False

        if self.expire_on_date and now() > self.expire_on_date:
            return False

        return True

    def custom_access_allowed(self, request):
        #OVERRIDE IN SUBCLASS
        return True