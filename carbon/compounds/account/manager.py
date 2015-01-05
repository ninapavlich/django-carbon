from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone


class UserQueryset(models.query.QuerySet):
    

    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):
    """
    ==================
    User Model Manager
    ==================

    Model manager for extending User Model methods.
    """

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a Super User using `create_user` and overriding permissions.
        """
        u = self.create_user(
            email,
            email,
            password,
            **extra_fields
        )
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
