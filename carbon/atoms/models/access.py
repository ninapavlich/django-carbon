import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstract import *


class AccessAtom(models.Model):

    help = {
        'access': "Access level",
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

    class Meta:
        abstract = True


# -- Level 4
class AccessKeyAtom(models.Model):
    auto_generate_key = True

    help = {
        'access_key': "Require access key to access this page.",
    }

    access_key = models.CharField(_("key"), max_length=50, blank=True,
                                  null=True, unique=True, help_text=help['access_key'])

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if self.auto_generate_key and not self.access_key:
            self.access_key = uuid.uuid1().hex

        super(AccessKeyAtom, self).save(*args, **kwargs)

    def get_access_key_session_key(self):
        return u'%s_access_key' % (self.uuid)

    def is_authorized(self, request):

        if(self.access_key):
            stored_password = request.session.get(self.get_access_key_session_key(), None)
            return stored_password == self.access_key

        return True

    def test_key(self, access_key):
        if access_key == self.access_key:
            return True
        return False

    def authorize_request(self, request):
        request.session[self.get_access_key_session_key()] = self.access_key

    def deauthorize_request(self, request):
        request.session[self.get_access_key_session_key()] = None


class AccessibleAtom(models.Model):

    help = {
        'require_registered_user': "Require logged in user"
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

    require_registered_user = models.BooleanField(_("Required Registered Users"),
                                                  default=False, help_text=help['require_registered_user'])

    # THOUGHT: Not sure if I love this design
    user_whitelist = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True, null=True, related_name='%(app_label)s_%(class)s_whitelist_user')

    user_blacklist = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            blank=True, null=True, related_name='%(app_label)s_%(class)s_blacklist_user')

    groups_whitelist = models.ManyToManyField('auth.Group',
                                              blank=True, null=True, related_name='%(app_label)s_%(class)s_whitelist_groups')

    groups_blacklist = models.ManyToManyField('auth.Group',
                                              blank=True, null=True, related_name='%(app_label)s_%(class)s_blacklist_groups')

    class Meta:
        abstract = True

    def is_authorized(self, request):

        if self.require_registered_user:
            if not request.user or not request.user.is_authenticated():
                return False

        if len(self.object.groups_whitelist.all()) > 0:
            # make sure user is allowed
            # TODO
            return False

        if len(self.object.groups_blacklist.all()) > 0:
            # make sure user is allowed
            # TODO
            return False

        if len(self.user_whitelist.all()) > 0:
            if not request.user or not request.user.is_authenticated() \
                    or not request.user in user_whitelist:
                return False

        if len(self.user_blacklist.all()) > 0:
            if not request.user or not request.user.is_authenticated() \
                    or request.user in user_blacklist:
                return False

        return True

    def custom_access_allowed(self, request):
        # OVERRIDE IN SUBCLASS
        return True
