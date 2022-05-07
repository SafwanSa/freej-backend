from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.campus.models import ResidentProfile, Campus
from apps.campus import queries as campusQueries
from typing import Iterable
import json


class EventService:

    @staticmethod
    def send_push_notification(event: Event, receivers: Iterable[ResidentProfile], title: str, body: str) -> None:
        if receivers.count() != 0:
            NotificationService.send(
                type=NotificationType.PushNotification,
                title=title,
                body=body,
                receivers=','.join([resident.user.username for resident in receivers]),
                data={
                    "type": "event",
                    "instance_id": event.id
                }
            )

    @staticmethod
    def create_event(resident_profile: ResidentProfile, type: str, name: str,
                     description: str, date: str, location_url: str = None, images: list = None) -> Event:
        campus = resident_profile.room.building.campus
        new_event = Event.objects.create(
            host=resident_profile,
            campus=campus,
            type=type,
            name=name,
            description=description,
            location_url=location_url,
            date=date,
            status=Event.EventStatus.Open.value
        )
        if images is not None and len(images) != 0:
            for url in images:
                new_image = EventImage.objects.create(
                    event=new_event,
                    image=url
                )
        campus_residents = campusQueries.get_all_campus_residents(campus=campus)
        EventService.send_push_notification(
            event=new_event,
            receivers=campus_residents,
            title=f'New event in {campus.name_en}',
            body="Don't miss it!"
        )
        return new_event

    @staticmethod
    def update_event(resident_profile: ResidentProfile, event: Event, type: str, name: str,
                     description: str, date: str, location_url: str = None, images: list = None) -> Event:
        if resident_profile != event.host:
            raise APIError(Error.EVENT_HOST_ONLY)
        event.name = name
        event.type = type
        event.description = description
        event.location_url = location_url
        event.date = date
        event.save()

        if images is not None and len(images) != 0:
            # Delete previous images
            old_images = queries.get_event_images(event=event)
            for img in old_images:
                img.delete()

            # Add new images
            for url in images:
                new_image = EventImage.objects.create(
                    event=event,
                    image=url
                )
        event_joiners = queries.get_event_joiners(event=event)
        EventService.send_push_notification(
            event=event,
            receivers=event_joiners,
            title=f'The event ({event.name}) has been changed',
            body="Check it out"
        )
        return event

    @staticmethod
    def delete_event(resident_profile: ResidentProfile, event: Event) -> Event:
        if resident_profile != event.host:
            raise APIError(Error.EVENT_HOST_ONLY)
        event.delete()
        event_joiners = queries.get_event_joiners(event=event)
        EventService.send_push_notification(
            event=event,
            receivers=event_joiners,
            title=f'The event ({event.name}) has been deleted :(',
            body="Sorry for that"
        )
        return event

    @staticmethod
    def join_event(resident_profile: ResidentProfile, event: Event) -> EventApplication:
        # Check if the resident has an application he cancelled
        application = queries.get_events_applications_by(
            resident_profile=resident_profile,
            event=event,
            status=None
        ).first()
        if application:
            if application.status == EventApplication.ApplicationStatus.Cancelled.value:
                application.status = EventApplication.ApplicationStatus.Joined.value
                application.save()
            return application
        else:
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
            status=EventApplication.ApplicationStatus.Joined
        )
        if applications.exists():
            application = applications.first()
            application.status = EventApplication.ApplicationStatus.Cancelled.value
            application.save()
            return application
        else:
            raise APIError(Error.NO_EVENT_APPLICATION)
