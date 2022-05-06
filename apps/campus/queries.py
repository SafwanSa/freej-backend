from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.post import queries as postQueries
from apps.event import queries as eventQueries
from apps.post.models import Post
from apps.event.models import Event


def get_all_campuses() -> Iterable[Campus]:
    return Campus.objects.filter(is_deleted=False).order_by('name_en')


def get_campus_by_id(id: int, with_deleted=False) -> Campus:
    try:
        if with_deleted:
            return Campus.objects_with_deleted.get(id=id)
        else:
            return Campus.objects.get(id=id)
    except Campus.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Campus._meta.model_name])


def get_all_campus_residents(campus: Campus) -> Iterable[ResidentProfile]:
    return ResidentProfile.objects.filter(is_deleted=False, room__building__campus=campus)


def get_campus_buildings(campus: Campus) -> Iterable[Building]:
    return campus.buildings.filter(is_deleted=False).order_by('name')


def get_building_by_id(id: int, with_deleted=False) -> Building:
    try:
        if with_deleted:
            return Building.objects_with_deleted.get(id=id)
        else:
            return Building.objects.get(id=id)
    except Building.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Building._meta.model_name])


def get_all_building_residents(building: Building) -> Iterable[ResidentProfile]:
    return ResidentProfile.objects.filter(is_deleted=False, room__building=building)


def get_building_rooms(building: Building) -> Iterable[Room]:
    return building.rooms.filter(is_deleted=False).order_by('name')


def get_room_by_id(id: int, with_deleted=False) -> Room:
    try:
        if with_deleted:
            return Room.objects_with_deleted.get(id=id)
        else:
            return Room.objects.get(id=id)
    except Room.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Room._meta.model_name])


def get_resident_profile_by(user: User) -> ResidentProfile:
    try:
        return ResidentProfile.objects.get(user=user)
    except ResidentProfile.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[ResidentProfile._meta.model_name])


def get_room_residents(room: Room) -> Iterable[ResidentProfile]:
    return room.residents.filter(is_deleted=False)


def get_issue_by_id(id: int, with_deleted=False) -> MaintenanceIssue:
    try:
        if with_deleted:
            return MaintenanceIssue.objects_with_deleted.get(id=id)
        else:
            return MaintenanceIssue.objects.get(id=id)
    except MaintenanceIssue.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[MaintenanceIssue._meta.model_name])


def get_building_issues(building: Building) -> Iterable[MaintenanceIssue]:
    return building.issues.filter(is_deleted=False).order_by('-created_at')


def get_resident_posts_by(resident_profile: ResidentProfile) -> Iterable[Post]:
    all_posts = postQueries.get_all_campus_posts(campus=resident_profile.room.building.campus)
    created_posts = resident_profile.created_posts.filter(is_deleted=False)
    applied_posts_ids = resident_profile.posts_applications.filter(is_deleted=False).values_list('post', flat=True)
    applied_posts = all_posts.filter(id__in=applied_posts_ids)
    return created_posts.union(applied_posts).order_by('-created_at')


def get_resident_events_by(resident_profile: ResidentProfile) -> Iterable[Event]:
    all_events = eventQueries.get_all_campus_events(campus=resident_profile.room.building.campus)
    hosted_events = resident_profile.hosted_events.filter(is_deleted=False)
    applied_events_ids = resident_profile.events_applications.filter(is_deleted=False).values_list('event', flat=True)
    applied_events = all_events.filter(id__in=applied_events_ids)
    return hosted_events.union(applied_events).order_by('-created_at')
