from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.abstract import VersionableAtom, TitleAtom, OrderedItemAtom
from carbon.atoms.models.content import ContentMolecule
from carbon.atoms.models.access import AccessAtom
from carbon.atoms.models.user import UserMolecule, StreetAddressMolecule, \
    UserProfileMolecule, SocialContactLinkMolecule

from .manager import UserManager

class User(UserProfileMolecule):

    objects = UserManager()

    class Meta:
        abstract = True


class Address(StreetAddressMolecule):

    class Meta:
        abstract = True

class UserGroup(ContentMolecule):

    def get_members(self):
        if not self.member_class:
            raise NotImplementedError('Class should specify an member_class')
        
        return self.member_class.objects.filter(group=self).order_by('order')

    class Meta:
        abstract = True
        ordering = ['order']

class UserGroupMember(VersionableAtom, OrderedItemAtom):

    class Meta:
        abstract = True
        ordering = ['order']

    # YOU MUST IMPLEMENT THIS:
    # group = models.ForeignKey('account.UserGroup', 
    #     blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True)


class Organization(ContentMolecule):

    class Meta:
        abstract = True

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True)

    def get_admins(self):
        return OrganizationMember.objects.filter(organization=self,access=AccessAtom.OWNER)

    def get_editors(self):
        return OrganizationMember.objects.filter(organization=self,access=AccessAtom.WRITE)

    def get_viewers(self):
        return OrganizationMember.objects.filter(organization=self,access=AccessAtom.READ)

class OrganizationMember(VersionableAtom, AccessAtom):

    class Meta:
        abstract = True

    # YOU MUST IMPLEMENT THIS:
    # organization = models.ForeignKey('Organization', 
    #     blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True)

class SocialContactLink(SocialContactLinkMolecule):
    class Meta:
        abstract = True