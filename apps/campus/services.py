import json
from typing import Iterable
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
    def send_push_notification(campus: Campus, receivers: Iterable[ResidentProfile], title: str, body: str) -> None:
        if len(receivers) != 0:
            NotificationService.send(
                type=NotificationType.PushNotification,
                title=title,
                body=body,
                receivers=','.join([resident.user.username for resident in receivers]),
                data={
                    "type": "campus",
                    "instance_id": campus.id
                }
            )

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
        NotificationService.send(
            type=NotificationType.Email,
            template='email/new_account.html',
            title='Welcome to freej',
            receivers=email,
            data=json.dumps({
                "email": email
            })
        )
        return new_resident_profile

    @staticmethod
    def edit_profile(resident_profile: ResidentProfile, first_name: str = None,
                     last_name: str = None, mobile_number: str = None, photo: str = None, room_id: int = None) -> ResidentProfile:
        user = resident_profile.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if mobile_number:
            user.mobile_number = mobile_number
        if photo:
            resident_profile.photo = photo
        if room_id:
            room = queries.get_room_by_id(id=room_id)
            if resident_profile.is_supervisor and room.building != resident_profile.room.building:
                raise APIError(Error.SUPERVISOR_CANNOT_CHANGE_ROOM)
            resident_profile.room = room
        user.save()
        resident_profile.save()
        return resident_profile

    @staticmethod
    def make_supervisor(resident_profile: ResidentProfile) -> None:
        resident_profile.is_supervisor = True
        resident_profile.save()
        group, created = Group.objects.get_or_create(name=GroupEnum.Supervisor.value)
        group.user_set.add(resident_profile.user)
        ResidentService.send_push_notification(
            campus=resident_profile.room.building.campus,
            receivers=[resident_profile],
            title='Congrats!. You was promoted',
            body='You are now the supervisor of your building'
        )

    @staticmethod
    def remove_supervisor(resident_profile: ResidentProfile) -> None:
        resident_profile.is_supervisor = False
        resident_profile.save()
        group, created = Group.objects.get_or_create(name=GroupEnum.Supervisor.value)
        group.user_set.remove(resident_profile.user)
        ResidentService.send_push_notification(
            campus=resident_profile.room.building.campus,
            receivers=[resident_profile],
            title='Sorry!. You was downgraded',
            body='You are now not the supervisor of your building'
        )


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

    @staticmethod
    def update_supervisor(building: Building) -> None:
        building_residents = queries.get_all_building_residents(building=building)
        for resident in building_residents:
            ResidentService.remove_supervisor(resident_profile=resident)
        if building.supervisor:
            ResidentService.make_supervisor(resident_profile=building.supervisor)

    @staticmethod
    def get_num_building_residents(building: Building) -> int:
        return queries.get_all_building_residents(building=building).count()

    @staticmethod
    def get_num_building_rooms(building: Building) -> int:
        return queries.get_building_rooms(building=building).count()

    @staticmethod
    def update_building(building: Building, whatsApp_link: str = None, location_url: str = None) -> Building:
        building.whatsApp_link = whatsApp_link
        building.location_url = location_url
        return building
