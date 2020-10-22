from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True
    
    def create_user(self, registration, firstname, lastname, organization, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not registration:
            raise ValueError(_('The registration must be set'))
        if not firstname:
            raise ValueError(_('User must have an firstname'))
        if not lastname:
            raise ValueError(_('User must have an firstname'))

        user = self.model(registration=registration,
                          firstname = firstname,
                          lastname = lastname,
                          organization = organization,
                          phone = phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        will be create later
        """
        pass

