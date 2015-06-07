from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

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

	class Meta:
		abstract = True


class AccessKeyAtom(models.Model):

	access_key = models.CharField(_("key"), max_length=50, blank=True, null=True, unique=True)

	def save(self, *args, **kwargs):

		if not self.access_key:
			self.access_key = uuid.uuid1().hex 

		super(AccessKeyAtom, self).save(*args, **kwargs)
		

	class Meta:
		abstract = True

# -- Level 4
class AccessibleAtom(models.Model):

	help = {
		'password':"Password to use if access_restriction is set to Password",
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

	

	class Meta:
		abstract = True

	def access_allowed(self, request):
		
		if self.require_registered_user: 
			if not request.user or not request.user.is_authenticated():
				return False

		if len(self.object.groups_whitelist.all()) > 0:
			#make sure user is allowed
			#TODO
			return False

		if len(self.object.groups_blacklist.all()) > 0:
			#make sure user is allowed 
			#TODO
			return False       

		if len(self.user_whitelist.all()) > 0:
			if not request.user or not request.user.is_authenticated() \
			or not request.user in user_whitelist:
				return False

		if len(self.user_blacklist.all()) > 0:
			if not request.user or not request.user.is_authenticated() \
			or request.user in user_blacklist:
				return False

		#TODO -- password

		
		return True

	def custom_access_allowed(self, request):
		#OVERRIDE IN SUBCLASS
		return True