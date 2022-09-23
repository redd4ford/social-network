from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

from domain.core.singleton_metaclass import Singleton


class DomainUserService(BaseUserManager, metaclass=type(Singleton)):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username, email=self.normalize_email(email), date_joined=timezone.now()
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user