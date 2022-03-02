from django.db import models
from apps.utility.models import BaseModel

# from pyfcm import FCMNotification
# from account.models import CustomUser, FCMToken


class Notification(BaseModel):
    type = models.CharField(max_length=5, choices=(
        ('Email', 'Email'),
        ('SMS', 'SMS')
    ))
    receivers = models.TextField(
        help_text="This takes a comma separated value. (e.g. example@1.com,example@2.com)")
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    template = models.CharField(max_length=255, null=True, blank=True)
    result = models.TextField(null=True, blank=True)
