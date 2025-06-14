from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, first_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, password):
        """Create a new superuser profile"""
        user = self.create_user(email, first_name, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class Account(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        """Return string representation of our user"""
        return self.email

    def get_full_name(self):
        """Retrieve full name of user"""
        return f"{self.first_name} {self.last_name}"
