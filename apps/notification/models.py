from django.db import models
from core.models import BaseModel
from enum import Enum
from core import utils
# from pyfcm import FCMNotification
# from account.models import CustomUser, FCMToken


class Notification(BaseModel):
    class NotificationType(Enum):
        SMS = 'SMS'
        Email = 'Email'
        PushNotification = 'PushNotification'
    type = models.CharField(max_length=50, choices=utils.create_choices_from_enum(NotificationType))
    receivers = models.TextField(
        help_text="This takes a comma separated value. (e.g. example@1.com,example@2.com)")
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    template = models.CharField(max_length=255, null=True, blank=True)
    result = models.TextField(null=True, blank=True)
