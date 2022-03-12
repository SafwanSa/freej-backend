from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from django.contrib.auth import password_validation
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User


class AccountService:
    pass


class AuthService:

    @staticmethod
    def optain_resident_access_token(user: User, token: dict) -> dict:
        if not user.groups.filter(name=GroupEnum.Resident.value).exists():
            raise APIError(Error.NO_ACTIVE_ACCOUNT)
        token['roles'] = list(user.groups.all().values())
        return token

    @staticmethod
    def optain_access_token(group: GroupEnum, user: User, token: dict) -> dict:
        if user.is_blocked:
            raise APIError(Error.BLOCKED_USER)

        if group == GroupEnum.Resident:
            return AuthService.optain_resident_access_token(user=user, token=token)
        else:
            raise APIError(Error.NO_ACTIVE_ACCOUNT)
