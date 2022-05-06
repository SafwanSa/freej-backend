from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.account.models import User
from apps.campus.models import Campus, Building


def get_all_announcements() -> Iterable[Announcement]:
    return Announcement.objects.filter(is_deleted=False).order_by('-created_at')


def get_announcement_by_id(id: int, with_deleted=False) -> Announcement:
    try:
        if with_deleted:
            return Announcement.objects_with_deleted.get(id=id)
        else:
            return Announcement.objects.get(id=id)
    except Announcement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Announcement._meta.model_name])


def get_announcements_by(sender: User, type: Announcement.AnnouncementType) -> Iterable[Announcement]:
    if type == Announcement.AnnouncementType.Campus:
        return CampusAnnouncement.objects.filter(sender=sender, is_deleted=False).order_by('-created_at')
    elif type == Announcement.AnnouncementType.Building:
        return BuildingAnnouncement.objects.filter(sender=sender, is_deleted=False).order_by('-created_at')
    else:
        return CommercialAnnouncement.objects.filter(sender=sender, is_deleted=False).order_by('-created_at')


def get_all_building_announcements() -> Iterable[BuildingAnnouncement]:
    return BuildingAnnouncement.objects.filter(is_deleted=False).order_by('-created_at')


def get_building_announcements(building: Building) -> Iterable[BuildingAnnouncement]:
    return building.announcements.filter(is_deleted=False).order_by('-created_at')


def get_building_announcement_by_id(id: int, with_deleted=False) -> BuildingAnnouncement:
    try:
        if with_deleted:
            return BuildingAnnouncement.objects_with_deleted.get(id=id)
        else:
            return BuildingAnnouncement.objects.get(id=id)
    except BuildingAnnouncement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[BuildingAnnouncement._meta.model_name])


def get_all_campus_announcements() -> Iterable[CampusAnnouncement]:
    return CampusAnnouncement.objects.filter(is_deleted=False).order_by('-created_at')


def get_campus_announcement_by_id(id: int, with_deleted=False) -> CampusAnnouncement:
    try:
        if with_deleted:
            return CampusAnnouncement.objects_with_deleted.get(id=id)
        else:
            return CampusAnnouncement.objects.get(id=id)
    except CampusAnnouncement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[CampusAnnouncement._meta.model_name])


def get_campus_announcements(campus: Campus) -> Iterable[CampusAnnouncement]:
    return campus.announcements.filter(is_deleted=False).order_by('-created_at')


def get_campus_commercial_announcements(campus: Campus) -> Iterable[CommercialAnnouncement]:
    return campus.commercial_announcements.filter(is_deleted=False).order_by('-created_at')


def get_all_commercial_announcements() -> Iterable[CommercialAnnouncement]:
    return CommercialAnnouncement.objects.filter(is_deleted=False).order_by('-created_at')


def get_commercial_announcement_by_id(id: int, with_deleted=False) -> CommercialAnnouncement:
    try:
        if with_deleted:
            return CommercialAnnouncement.objects_with_deleted.get(id=id)
        else:
            return CommercialAnnouncement.objects.get(id=id)
    except CommercialAnnouncement.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[CommercialAnnouncement._meta.model_name])
