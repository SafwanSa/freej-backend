from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError


def get_all_campuses() -> Iterable[Campus]:
    return Campus.objects.filter(is_deleted=False)


def get_campus_by_id(id: int) -> Campus:
    try:
        return Campus.objects.get(id=id)
    except Campus.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Campus._meta.model_name])


def get_campus_buildings(campus: Campus) -> Iterable[Building]:
    return campus.buildings.filter(is_deleted=False)


def get_building_by_id(id: int) -> Building:
    try:
        return Building.objects.get(id=id)
    except Building.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Building._meta.model_name])


def get_building_rooms(building: Building) -> Iterable[Room]:
    return building.rooms.filter(is_deleted=False)


def get_room_by_id(id: int) -> Room:
    try:
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
