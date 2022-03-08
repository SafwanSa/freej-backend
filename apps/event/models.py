from django.db import models
from apps.utility.models import BaseModel
from apps.campus.models import ResidentProfile
from enum import Enum
from core import utils


class Event(BaseModel):
    class EventType(Enum):
        Study = 'study'
        HelpSession = 'Help Session'
        Sport = 'sport'
        Game = 'game'
        Other = 'other'

    class EventStatus(Enum):
        New = 'new'
        Cancelled = 'cancelled'
        Finished = 'finished'
    host = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='hosted_events')
    type = models.CharField(max_length=30, choices=utils.create_choices_from_enum(EventType))
    name = models.CharField(max_length=100)
    description = models.TextField()
    location_url = models.URLField(null=True, blank=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=30, choices=utils.create_choices_from_enum(EventStatus))


class EventApplication(BaseModel):
    class ApplicationStatus(Enum):
        Joined = 'joined'
        Cancelled = 'cancelled'
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='applied_events')
    status = models.CharField(max_length=30, choices=utils.create_choices_from_enum(ApplicationStatus))
