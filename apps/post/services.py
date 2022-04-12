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
    def create_offer(resident_profile: ResidentProfile, title: str, description: str) -> Post:
        campus = resident_profile.room.building.campus
        new_offer = Post.objects.create(
            type=Post.PostType.Offer.value,
            campus=campus,
            owner=resident_profile,
            title=title,
            description=description,
        )
        return new_offer


class RequestService(PostService):

    @staticmethod
    def create_request():
        pass
