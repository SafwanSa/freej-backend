from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from django.contrib.auth import password_validation
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Building
from django.contrib.auth.models import Group


class AnnouncementService:

    @staticmethod
    def send_building_announcement(resident_profile: ResidentProfile, building: Building,
                                   title: str, body: str) -> BuildingAnnouncement:
        new_announcement = BuildingAnnouncement.objects.create(
            sender=resident_profile.user,
            building=building,
            type=BuildingAnnouncement.AnnouncementType.Building.value,
            title=title,
            body=body
        )
        # TODO: Send FCM notifications to building's residents
        return new_announcement

    @staticmethod
    def delete_building_announcement(announcement=BuildingAnnouncement) -> BuildingAnnouncement:
        announcement.is_deleted = True
        announcement.save()
        return announcement
