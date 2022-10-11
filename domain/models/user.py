from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin

from domain.services.user import DomainUserService
from domain.core.models import BasePKModel


class User(ExportModelOperationsMixin('user'), BasePKModel,
           AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        blank=False,
        null=False,
        editable=False
    )
    last_request_time = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    add_fieldsets = (
        None, {'fields': (
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
            'date_joined',
            'last_request_time'
        )
        }
    )

    objects = DomainUserService()

    class Meta:
        app_label = 'domain'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id} {self.email} ({self.get_full_name()})'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.username}'

    def _generate_jwt_token(self):
        dt = timezone.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
