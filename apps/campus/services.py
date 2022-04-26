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
    def create_resident_profile(email: str, password: str, otp: str, room_id: int,
                                name: str, mobile_number: str) -> ResidentProfile:
        # OTP Check
        otp = AuthService.check_otp(username=email, otp=otp)
        # Register the user again for validation again
        AccountService.register_resident(
            email=email,
            password=password,
            room_id=room_id,
            name=name,
            mobile_number=mobile_number,
            send_otp=False,
        )
        # Create user account
        user = AccountService.create_account(username=email, password=password, name=name, mobile_number=mobile_number)
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
        return new_resident_profile

    @staticmethod
    def edit_profile(resident_profile: ResidentProfile, first_name: str = None,
                     last_name: str = None, mobile_number: str = None, photo: str = None) -> ResidentProfile:
        user = resident_profile.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if mobile_number:
            user.mobile_number = mobile_number
        if photo:
            resident_profile.photo = photo
        user.save()
        resident_profile.save()
        return resident_profile


class BuildingService:

    @staticmethod
    def report_issue(resident_profile: ResidentProfile, building: Building,
                     type: str, description: str) -> MaintenanceIssue:
        new_issue = MaintenanceIssue.objects.create(
            reported_by=resident_profile,
            building=building,
            type=type,
            description=description,
            status=MaintenanceIssue.MaintenanceIssueStatus.Pending.value
        )
        return new_issue

    @staticmethod
    def report_issue_with_fix(issue: MaintenanceIssue, resident_profile: ResidentProfile) -> MaintenanceIssue:
        # Check if the resident has already reported a fix issue
        reporters = issue.reported_fixed_by.all()
        if resident_profile in reporters:
            raise APIError(Error.ALREADY_FIXED_REPORTED)
        # Add the resident to the reporters
        issue.reported_fixed_by.add(resident_profile)
        issue.reported_fixed = issue.reported_fixed + 1
        issue.save()
        return issue
