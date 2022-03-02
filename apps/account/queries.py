from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError


def get_users() -> Iterable[User]:
    return User.objects.all()
