from apps.utility.models import BaseModel
from django.db import models
from apps.account.models import User
from enum import Enum
from core import utils


class Campus(BaseModel):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    email_domain = models.CharField(max_length=50, null=True, blank=True)
    # TODO: Add location_url?
    # TODO: Add image?

    def __str__(self) -> str:
        return self.name_en


class Building(BaseModel):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=10)
    # TODO: Add location_url?
    # TODO: Add image?
    supervisor = models.OneToOneField(
        'campus.ResidentProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_building')
    whatsApp_link = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.campus.name_en}-{self.name}'


class Room(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.building}-{self.name}'


class ResidentProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resident_profile')
    # TODO: Add photo
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='residents')
    is_supervisor = models.BooleanField(default=False)


class MaintenanceIssue(BaseModel):
    class MaintenanceIssueType(Enum):
        Halls = 'halls'
        Rooms = 'Rooms'
        Bathrooms = 'bathroom'
        Other = 'other'

    class MaintenanceIssueStatus(Enum):
        Pending = 'Pending'
        Canceled = 'canceled'
        Fixed = 'fixed'
    reported_by = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='reported_issues')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='issues')
    type = models.CharField(max_length=30, choices=utils.create_choices_from_enum(MaintenanceIssueType))
    description = models.TextField()
    reported_fixed = models.IntegerField(default=0)
    status = models.CharField(max_length=30, choices=utils.create_choices_from_enum(MaintenanceIssueStatus))
