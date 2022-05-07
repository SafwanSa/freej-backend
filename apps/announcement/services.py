import json
from typing import Iterable
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
    def send_push_notification(announcement: Announcement,
                               receivers: Iterable[ResidentProfile], title: str, body: str) -> None:
        if len(receivers) != 0:
            NotificationService.send(
                type=NotificationType.PushNotification,
                title=title,
                body=body,
                receivers=','.join([resident.user.username for resident in receivers]),
                data={
                    "type": "announcement",
                    "instance_id": announcement.id
                }
            )

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
        AnnouncementService.send_push_notification(
            announcement=new_announcement,
            receivers=building_residents,
            title=title,
            body=body
        )
        return new_announcement

    @staticmethod
    def delete_building_announcement(announcement=BuildingAnnouncement) -> BuildingAnnouncement:
        announcement.delete()
        return announcement

    @staticmethod
    def record_impression(announcement=CommercialAnnouncement) -> None:
        if announcement.type == Announcement.AnnouncementType.Advertisement.value:
            announcement.impressions += 1
            announcement.save()
