from django.db import models
from core.models import BaseModel
from enum import Enum
from core import utils
from apps.campus.models import ResidentProfile
from apps.account.models import User


class Report(BaseModel):
    class InstanceType(Enum):
        Announcement = 'announcement'
        Event = 'event'
        Post = 'post'

        @classmethod
        def has_member_key(cls, key):
            match = False
            for value in cls:
                if key.lower() == value.value.lower():
                    match = True
            return match
    reporter = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='reports')
    instance_type = models.CharField(max_length=50, choices=utils.create_choices_from_enum(InstanceType))
    instance_id = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    is_checked = models.BooleanField(default=False)
    checked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='checked_reports',
        null=True,
        blank=True
    )
