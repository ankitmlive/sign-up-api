from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    registration = models.EmailField(verbose_name='registration', max_length=255, unique=True,)
    firstname = models.CharField(verbose_name='first name', max_length=50, blank=True)
    lastname = models.CharField(verbose_name='last name', max_length=50, blank=True)
    organization = models.CharField(verbose_name='phone', max_length=100, blank=True)
    phone = models.CharField(verbose_name='phone', max_length=50, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin
    # is_staff can be removed if not using Django Admin
    # is_admin can be removed if not using Django Admin

    objects = CustomUserManager()

    USERNAME_FIELD = 'registration'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    #email & password is auto required , no need to implement in REQUIRED_FIELD 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
