from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from enum import Enum
from core.validators import _PHONE_REGEX, _STUDENT_ID_REGEX


class GroupEnum(Enum):
    Admin = 'Admin'
    Resident = 'Resident'
    Supervisor = 'Supervisor'


class User(AbstractUser):
    username = models.CharField(max_length=9, unique=True, validators=[_STUDENT_ID_REGEX])
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10, validators=[_PHONE_REGEX], null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
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

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.email = f's{self.username}@kfupm.edu.sa'
        return super().save(*args, **kwargs)
