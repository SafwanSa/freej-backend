from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from datetime import datetime


def get_users() -> Iterable[User]:
    return User.objects.all()


def get_users_with(username: str) -> Iterable[User]:
    return User.objects.filter(username=username)


def get_active_otp_with(username: str, otp: str) -> OTP:
    return OTP.objects.get(username=username, otp=otp, is_active=True, expiration_date__gte=datetime.now())


def get_active_requested_otps_of(username: str) -> OTP:
    return OTP.objects.filter(username=username, is_active=True)
