from django.db import models
from django.conf import settings

from carbon.compounds.account.models import User as BaseUser
from carbon.compounds.account.models import Address as BaseAddress
from carbon.compounds.account.models import Organization as BaseOrganization
from carbon.compounds.account.models import OrganizationMember as BaseOrganizationMember


class User(BaseUser):

    pass

class Address(BaseAddress):

    pass

class Organization(BaseOrganization):

    pass

class OrganizationMember(BaseOrganizationMember):

    organization = models.ForeignKey('Organization', blank=True, null=True)