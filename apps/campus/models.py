from apps.utility.models import BaseModel
from django.db import models
from apps.account.models import User


class Campus(BaseModel):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    # TODO: Add location_url?
    # TODO: Add image?


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


class Room(BaseModel):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=10)


class ResidentProfile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resident_profile')
    # TODO: Add photo
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='residents')
    is_supervisor = models.BooleanField(default=False)
