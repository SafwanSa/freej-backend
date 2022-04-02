from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.campus.models import ResidentProfile


def get_all_campus_events(campus: Campus) -> Iterable[Event]:
    return campus.events.filter(is_deleted=False)


def get_campus_events_by_status(campus: Campus, status: Event.EventStatus) -> Iterable[Event]:
    return campus.events.filter(is_deleted=False, status=status)


def get_event_by_id(id: int) -> Event:
    try:
        return Event.objects.get(id=id)
    except Event.DoesNotExist:
        raise APIError(Error.INSTANCE_NOT_FOUND, extra=[Event._meta.model_name])


def get_all_event_applications(event: Event) -> Iterable[EventApplication]:
    return event.applications.filter(is_deleted=False)


def get_event_applications_by_status(event: Event, status=Event.EventStatus) -> Iterable[EventApplication]:
    return event.applications.filter(is_deleted=False, status=status)


def get_all_applied_events_of(resident_profile: ResidentProfile) -> Iterable[Event]:
    return resident_profile.events_applications.filter(is_deleted=False)


def get_events_applications_by(resident_profile: ResidentProfile, event: Event,
                               status: EventApplication.ApplicationStatus = None) -> Iterable[Event]:
    if not status:
        return resident_profile.events_applications.filter(is_deleted=False, event=event)
    return resident_profile.events_applications.filter(is_deleted=False, event=event, status=status.value)
