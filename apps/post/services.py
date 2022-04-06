from django.utils import timezone
from .models import *
from core.errors import APIError, Error
from . import queries
from apps.notification.services import NotificationService, NotificationType
from apps.account.models import GroupEnum, User
from apps.campus.models import ResidentProfile, Campus


class PostService:

    @staticmethod
    def create_post():
        pass


class OfferService(PostService):

    @staticmethod
    def create_offer():
        pass


class RequestService(PostService):

    @staticmethod
    def create_request():
        pass
