from django.db import models
from core.models import BaseModel
from apps.account.models import User
from apps.campus.models import Building, Campus
from enum import Enum
from core import utils
import time


class Announcement(BaseModel):
    class AnnouncementType(Enum):
        Campus = 'campus'
        Building = 'building'
        Advertisement = 'advertisement'

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=utils.create_choices_from_enum(AnnouncementType))
    title = models.CharField(max_length=100)
    body = models.TextField()


class BuildingAnnouncement(Announcement):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='announcements')


class CampusAnnouncement(Announcement):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='announcements')


class CommercialAnnouncement(Announcement):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='commercial_announcements')
    impressions = models.IntegerField(default=0)
    advertiser_name = models.CharField(max_length=50)
    image = models.FileField(
        upload_to=utils.PathAndRename(
            'uploads/commercials/images/{}'.format(time.strftime("%Y/%m/%d"))),
        max_length=2048,
        blank=True, null=True
    )
    link = models.URLField(null=True, blank=True)
