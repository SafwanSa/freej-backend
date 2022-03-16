from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
from core.validators import _PHONE_REGEX, _STUDENT_ID_REGEX
from apps.utility.models import BaseModel
from core import utils
from datetime import datetime, timedelta
from apps.utility.services import ConfigService as Conf
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager,
)
from django.utils import timezone


class GroupEnum(Enum):
    Admin = 'Admin'
    Resident = 'Resident'
    Supervisor = 'Supervisor'


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given email must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    username = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10, validators=[_PHONE_REGEX], null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    lang = models.CharField(
        max_length=2,
        choices=(
            ('en', 'en'),
            ('ar', 'ar'),
        ),
        default='ar'
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        return super().save(*args, **kwargs)


class OTP(BaseModel):
    username = models.EmailField()
    is_active = models.BooleanField(default=True)
    otp = models.CharField(max_length=4)
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.otp = utils.generate_otp()
        self.expiration_date = datetime.now() + timedelta(seconds=Conf.OTP_EXPIRATION())
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.otp
