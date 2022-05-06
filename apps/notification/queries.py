from .models import *
from django.db.models import Q
from typing import Iterable
from core.errors import Error, APIError
from apps.campus.models import ResidentProfile


def get_push_notifications_by(resident_profile: ResidentProfile) -> Iterable[Notification]:
    email = resident_profile.user.username
    return Notification.objects.filter(
        type=Notification.NotificationType.PushNotification.value, receivers__icontains=email).order_by('-created_at')
