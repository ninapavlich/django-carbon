from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.abstract import VersionableAtom
from carbon.atoms.models.access import AccessAtom
from carbon.atoms.models.user import UserMolecule, StreetAddressMolecule

from .manager import UserManager

class User(UserMolecule):

    objects = UserManager()

    class Meta:
        abstract = True


class Address(StreetAddressMolecule):

    class Meta:
        abstract = True


class Organization(VersionableAtom):

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

    organization = models.ForeignKey('Organization', 
        blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        blank=True, null=True)