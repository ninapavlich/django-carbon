from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.functional import cached_property

from .abstract import *
from .access import *
from .content import *

from carbon.utils.icons import ICON_CHOICES


class PersonAtom(models.Model):

    help = {
        'first_name': "",
        'last_name':"",
    }

    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    middle_name = models.CharField(_('Middle name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)

    
    class Meta:
        abstract = True

class StreetAddressAtom(models.Model):

    street_1 = models.CharField(_('Street Address 1'), max_length=30, blank=True, null=True)
    street_2 = models.CharField(_('Street Address 2'), max_length=30, blank=True, null=True)
    city = models.CharField(_('City'), max_length=30, blank=True, null=True)
    state = models.CharField(_('State'), max_length=30, blank=True, null=True)
    zipcode = models.CharField(_('Zipcode'), max_length=30, blank=True, null=True)   

    latitude = models.CharField(_('Latitude'), max_length=30, blank=True, null=True)   
    longitude = models.CharField(_('Longitude'), max_length=30, blank=True, null=True)    
    
    class Meta:
        abstract = True     


class PhoneContactAtom(models.Model):
    class Meta:
        abstract = True 

    home_phone = models.CharField(_('Home Phone'), max_length=255, blank=True, null=True) 
    work_phone = models.CharField(_('Work Phone'), max_length=255, blank=True, null=True) 
    cell_phone = models.CharField(_('Cell Phone'), max_length=255, blank=True, null=True)




class StreetAddressMolecule(VersionableAtom, StreetAddressAtom):
    class Meta:
        abstract = True

class UserMolecule(VersionableAtom, PersonAtom, AbstractBaseUser, PermissionsMixin):
    help = {
        'email':"",
    }

    email = models.EmailField(_('email address'), unique=True, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'

    @staticmethod
    def autocomplete_search_fields():
        return ("email__icontains", "first_name__icontains", "middle_name__icontains", "last_name__icontains")

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_public_name(self):
        if self.first_name:
            return self.first_name
        return 'Anonymous User'

    def get_full_name(self):
        if self.first_name and self.last_name:
            return u"%s %s" % (self.first_name, self.last_name)
        elif self.first_name:
            return u"%s (%s)" % (self.first_name, self.email)
        elif self.last_name:
            return u"%s (%s)" % (self.first_name, self.email)
        else:
            return self.email

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        abstract = True

class UserProfileMolecule(UserMolecule, HasImageAtom):

    help = {
        'about':"",
    }

    about = models.TextField(_('about'), help_text=help['about'], null=True, blank=True)


    class Meta:
        abstract = True

class SocialContactLinkMolecule( VersionableAtom, TitleAtom, OrderedItemAtom, LinkAtom):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True)
    
    icon = models.CharField(max_length=255, null=True, blank=True, choices=ICON_CHOICES, 
        help_text='Preview icons at http://fontawesome.io/icons/',)  
    
    class Meta:
        abstract = True