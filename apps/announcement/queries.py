from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.account.models import User


def get_all_announcements() -> Iterable[Announcement]:
    return Announcement.objects.filter(is_deleted=False)


def get_announcement_by_id(id: int) -> Announcement:
    try:
        return Announcement.objects.get(id=id)
    except Announcement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Announcement._meta.model_name])


def get_announcements_by(sender: User, type: Announcement.AnnouncementType) -> Iterable[Announcement]:
    if type == Announcement.AnnouncementType.Campus:
        return CampusAnnouncement.objects.filter(sender=sender, is_deleted=False)
    elif type == Announcement.AnnouncementType.Building:
        return BuildingAnnouncement.objects.filter(sender=sender, is_deleted=False)
    else:
        return CommercialAnnouncement.objects.filter(sender=sender, is_deleted=False)


def get_all_building_announcements() -> Iterable[BuildingAnnouncement]:
    return BuildingAnnouncement.objects.filter(is_deleted=False)


def get_building_announcement_by_id(id: int) -> BuildingAnnouncement:
    try:
        return BuildingAnnouncement.objects.get(id=id)
    except BuildingAnnouncement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[BuildingAnnouncement._meta.model_name])


def get_all_campus_announcements() -> Iterable[CampusAnnouncement]:
    return CampusAnnouncement.objects.filter(is_deleted=False)


def get_campus_announcement_by_id(id: int) -> CampusAnnouncement:
    try:
        return CampusAnnouncement.objects.get(id=id)
    except CampusAnnouncement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[CampusAnnouncement._meta.model_name])


def get_all_commercial_announcements() -> Iterable[CommercialAnnouncement]:
    return CommercialAnnouncement.objects.filter(is_deleted=False)


def get_commercial_announcement_by_id(id: int) -> CommercialAnnouncement:
    try:
        return CommercialAnnouncement.objects.get(id=id)
    except CommercialAnnouncement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[CommercialAnnouncement._meta.model_name])
