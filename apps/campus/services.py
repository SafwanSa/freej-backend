from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from django.contrib.auth import password_validation
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.account.services import AuthService, AccountService
from django.contrib.auth.models import Group


class ResidentService:

    @staticmethod
    def create_resident_profile(email: str, password: str, otp: str, room_id: int) -> User:
        # OTP Check
        otp = AuthService.check_otp(username=email, otp=otp)
        # Register the user again for validation again
        AccountService.register_resident(
            email=email,
            password=password,
            room_id=room_id,
            send_otp=False,
        )
        # Create user account
        user = AccountService.create_account(username=email, password=password)
        # Assgin the user to a group
        group, created = Group.objects.get_or_create(name=GroupEnum.Resident.value)
        group.user_set.add(user)
        room = queries.get_room_by_id(id=room_id)
        # Create a resident profile
        new_resident_profile = ResidentProfile.objects.create(
            user=user,
            room=room,
            is_supervisor=False,
        )
        # TODO: Send notification that account was created
        return user
