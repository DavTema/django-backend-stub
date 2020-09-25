import os
import binascii

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.postgres.indexes import BrinIndex

from api.models.mixins import EditedDatesMixin


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserAccount(EditedDatesMixin, AbstractBaseUser, PermissionsMixin):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    email = models.EmailField(
        verbose_name=_('Email address'),
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=150,
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(
        verbose_name=_('Staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
    )

    objects = UserAccountManager()

    def get_full_name(self):
        return f'{self.first_name or ""} {self.last_name or ""}'.strip()

    class Meta:
        db_table = 'client_user_account'
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ('-created_at', )
        indexes = (
            BrinIndex(fields=('created_at',)),
        )


class CustomToken(EditedDatesMixin, models.Model):
    key = models.CharField(
        verbose_name=_('Key'),
        max_length=40,
        primary_key=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='auth_token',
    )

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    class Meta:
        db_table = 'client_token'
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')
