import json
from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Building
from apps.campus import queries as campusQueries
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
        building_residents = campusQueries.get_all_building_residents(building=building)
        NotificationService.send(
            type=NotificationType.PushNotification,
            title=title,
            body=body,
            receivers=','.join([resident.user.username for resident in building_residents]),
            data=json.loads({
                'type': 'announcement',
                "instance_id": new_announcement.id
            })
        )
        return new_announcement

    @staticmethod
    def delete_building_announcement(announcement=BuildingAnnouncement) -> BuildingAnnouncement:
        announcement.delete()
        return announcement
