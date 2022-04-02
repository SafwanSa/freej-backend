from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from django.contrib.auth import password_validation
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.account.services import AuthService, AccountService
from django.contrib.auth.models import Group
from apps.campus.models import ResidentProfile, Campus


class EventService:

    @staticmethod
    def create_event(resident_profile: ResidentProfile, type: str, name: str,
                     description: str, date: str, location_url: str = None) -> Event:
        campus = resident_profile.room.building.campus
        new_event = Event.objects.create(
            host=resident_profile,
            campus=campus,
            type=type,
            name=name,
            description=description,
            location_url=location_url,
            date=date,
            status=Event.EventStatus.New.value
        )
        # TODO: Notify all residents of campus
        return new_event

    @staticmethod
    def update_event(resident_profile: ResidentProfile, event: Event, type: str, name: str,
                     description: str, date: str, location_url: str = None) -> Event:
        if resident_profile != event.host:
            raise APIError(Error.EVENT_HOST_ONLY)
        event.name = name
        event.type = type
        event.description = description
        event.location_url = location_url
        event.date = date
        event.save()
        # TODO: Notify all joiners
        return event

    @staticmethod
    def delete_event(resident_profile: ResidentProfile, event: Event) -> Event:
        if resident_profile != event.host:
            raise APIError(Error.EVENT_HOST_ONLY)
        event.is_deleted = True
        event.save()
        # TODO: Notify all joiners
        return event

    @staticmethod
    def join_event(resident_profile: ResidentProfile, event: Event) -> EventApplication:
        new_application = EventApplication.objects.create(
            resident_profile=resident_profile,
            event=event,
            status=EventApplication.ApplicationStatus.Joined.value
        )
        return new_application

    @staticmethod
    def leave_event(resident_profile: ResidentProfile, event: Event) -> EventApplication:
        applications = queries.get_events_applications_by(
            resident_profile=resident_profile,
            event=event,
            status=EventApplication.ApplicationStatus.Joined)
        if applications.exists():
            application = applications.first()
            application.status = EventApplication.ApplicationStatus.Cancelled.value
            application.save()
            return application
        else:
            raise APIError(Error.NO_EVENT_APPLICATION)
