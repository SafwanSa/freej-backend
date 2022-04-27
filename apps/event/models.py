from django.db import models
from core.models import BaseModel
from apps.campus.models import ResidentProfile, Campus
from enum import Enum
from core import utils


class Event(BaseModel):
    class EventType(Enum):
        Study = 'study'
        HelpSession = 'helpSession'
        Sport = 'sport'
        Game = 'game'
        Other = 'other'

    class EventStatus(Enum):
        Open = 'open'
        Cancelled = 'cancelled'
        Finished = 'finished'
    host = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='hosted_events')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='events')
    type = models.CharField(max_length=30, choices=utils.create_choices_from_enum(EventType))
    name = models.CharField(max_length=100)
    description = models.TextField()
    location_url = models.URLField(null=True, blank=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=30, choices=utils.create_choices_from_enum(EventStatus))

    def __str__(self) -> str:
        return f'{self.campus}-{self.name}'


class EventImage(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()


class EventApplication(BaseModel):
    class ApplicationStatus(Enum):
        Joined = 'joined'
        Cancelled = 'cancelled'
    resident_profile = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='events_applications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=utils.create_choices_from_enum(ApplicationStatus))
