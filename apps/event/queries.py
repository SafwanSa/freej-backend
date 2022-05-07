from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.campus.models import Building, ResidentProfile


def get_all_campus_events(campus: Campus) -> Iterable[Event]:
    return campus.events.filter(is_deleted=False).order_by('-created_at')


def get_campus_events_by_status(campus: Campus, status: Event.EventStatus) -> Iterable[Event]:
    return campus.events.filter(is_deleted=False, status=status).order_by('-created_at')


def get_event_by_id(id: int, with_deleted=False) -> Event:
    try:
        if with_deleted:
            return Event.objects_with_deleted.get(id=id)
        else:
            return Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Event._meta.model_name])


def get_all_event_applications(event: Event) -> Iterable[EventApplication]:
    return event.applications.filter(is_deleted=False).order_by('-created_at')


def get_event_applications_by_status(event: Event, status=Event.EventStatus) -> Iterable[EventApplication]:
    return event.applications.filter(is_deleted=False, status=status).order_by('-created_at')


def get_event_joiners(event: Event) -> Iterable[ResidentProfile]:
    residents_ids = event.applications.filter(
        is_deleted=False,
        status=EventApplication.ApplicationStatus.Joined.value
    ).values_list('resident_profile', flat=True)
    return ResidentProfile.objects.filter(id__in=residents_ids)


def get_events_applications_by(resident_profile: ResidentProfile, event: Event,
                               status: EventApplication.ApplicationStatus = None) -> Iterable[Event]:
    if not status:
        return resident_profile.events_applications.filter(is_deleted=False, event=event).order_by('-created_at')
    return resident_profile.events_applications.filter(
        is_deleted=False, event=event, status=status.value).order_by('-created_at')


def get_event_images(event: Event) -> Iterable[EventImage]:
    return event.images.filter(is_deleted=False)


def get_events_by_building(building=Building) -> int:
    return Event.objects.filter(host__room__building=building)
